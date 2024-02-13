from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import *

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = user.cart  

        if cart.products.exists():
            total_price = cart.total_price() 
            order = Order.objects.create(user=user, cart=cart, total_price=total_price)
            cart.products.clear()

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=201)
        else:
            return Response('Cart is empty', status=40)
