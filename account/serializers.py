from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code
from django.core.mail import send_mail

User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True,
                    write_only=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False, write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_brand = serializers.BooleanField(default=False)
    brand = serializers.CharField(max_length=40)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь существует')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user
    

class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')

        if not User.objects.filter(email=email, activation_code=code).exists(): 
            raise serializers.ValidationError('User not found')
        return attrs
    
    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User not found'
            )
        return email
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        if email and password:
            user = authenticate(
                request, 
                email=email, 
                password=password 
                )
            if not user:
                raise serializers.ValidationError(
                    'Incorrect email or password'
                )
        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8, required=True)
    new_password = serializers.CharField(min_length=8, required=True)
    new_password_confirm = serializers.CharField(min_length=8, required=True)


    def validate_old_password(self, old_pass):
        user = self.context.get('request').user
        if not user.check_password(old_pass):
            raise serializers.ValidationError(
                'Введите правильный пароль'
            )
        return old_pass
    
    
    def validate(self, attrs):
        new_pass1 = attrs.get('new_password')
        new_pass2 = attrs.get('new_password_confirm')
        old_pass = attrs.get('old_password')

        if new_pass1 != new_pass2:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        
        if old_pass == new_pass1:
            raise serializers.ValidationError(
                'Пароли совпадают'
            )
        
        return attrs
    
    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.get(email=email):
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return email
    
    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Восстановление пароля',
            f'Ваш код восстановления: {user.activation_code}',
            'test@gmail.com',
            [email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    password = serializers. CharField(required=True, min_length=8)
    password_confirm = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        p1 = attrs.get('password')
        p2 = attrs.get('password_confirm')

        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError(
                'Пользователь не найдет'
            )
        if p1 != p2:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return attrs
    

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_passwor(password)
        user.activation_code = ''
        user.save()

