from rest_framework import viewsets
from .models import Order
from .serializers import *
from product.permissions import *

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthorPermission]