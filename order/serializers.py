from rest_framework.serializers import ModelSerializer, ReadOnlyField, ValidationError
from .models import Order

class OrderSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.name')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        cart = user.cart  
        validated_data['user'] = user

        if cart.products.exists():
            total_price = cart.total_price() 
            order = Order.objects.create(user=user, cart=cart, total_price=total_price)
            cart.products.clear()
            return order
        else:
            raise ValidationError('Cart is empty')

