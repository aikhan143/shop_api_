from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from product.serializers import ProductListSerializer
from . import tasks
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

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
    payment_link = ReadOnlyField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'created_at', 'payment_link']

    def create_payment_link(self, validated_data):
        request = self.context.get('request')
        user = request.user
        cart = user.cart
        product_title = cart.products.first().title  
        product_description = cart.products.first().description 
        amount = cart.total_price()

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_title,
                            'description': product_description,
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel'
            )

            return session.url

        except stripe.error.StripeError as e:
            return f'Error: {str(e)}'
        
    def get_payment_link(self, instance):
        if instance.payment_link:
            return instance.payment_link
        return self.create_payment_link(instance)
        
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        cart = user.cart  
        validated_data['user'] = user

        if cart.products.exists():
            total_price = cart.total_price() 
            order = Order.objects.create(user=user, cart=cart, total_price=total_price)
            order.create_verification_code()
            tasks.send_order_details(user.email, order, order.verification_code)
            return order
        else:
            raise ValidationError('Cart is empty')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = ProductListSerializer(instance.cart.products.all(), many=True).data
        representation['payment_link'] = self.get_payment_link(instance)
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