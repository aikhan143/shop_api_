from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from product.serializers import ProductListSerializer
from .utils import send_order_details

class CartProductSerializer(ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity', 'total_price']

class CartSerializer(ModelSerializer):
    from product.serializers import ProductSerializer
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['products', 'total_price']

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

class OrderSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.name')
    total_price = ReadOnlyField(source='cart.total_price')
    
    class Meta:
        model = Order
        fields = ['user', 'total_price', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        cart = user.cart  
        validated_data['user'] = user

        if cart.products.exists():
            total_price = cart.total_price() 
            order = Order.objects.create(user=user, cart=cart, total_price=total_price)
            order.create_verification_code()
            send_order_details(user.email, order, order.verification_code)
            return order
        else:
            raise ValidationError('Cart is empty')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = ProductListSerializer(instance.cart.products.all(), many=True).data
        return representation

class VerificationSerializer(ModelSerializer):
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'verification_code']

    def validate(self, attrs):
        user = attrs.get('user')
        code = attrs.get('verification_code')

        if not Order.objects.filter(user=user, verification_code=code).exists(): 
            raise ValidationError('Order not found')
        return attrs
    
    def verify(self):
        user = self.validated_data.get('user')
        order = Order.objects.get(user=user)
        order.is_verified = True
        order.verification_code = ''
        order.save()