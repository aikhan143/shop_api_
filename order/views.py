from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from product.permissions import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import generics


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(user=user).order_by('updated_at')
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        else:
            self.permission_classes = []
        return super().get_permissions()
    
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        user = request.user
        product = Product.objects.get(slug=pk)

        cart = Cart.objects.get(user=user)

        cart_product, product_created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if not product_created:
            cart_product.quantity += 1
            cart_product.save()

        serializer = CartProductSerializer(cart_product)
        return Response(serializer.data, status=201)
<<<<<<< HEAD
    
=======

>>>>>>> d536f0dcbb14e0184cb9022045cc5853356537fe
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthorPermission]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user).order_by('created_at')
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'completed'
        instance.cart.clear_cart()
        instance.delete()
        return Response('Order completed successfully', status=204)
        
class VerificationViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = VerificationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.verify()
        return Response(serializer.data, status=200)

# class OrderHistoryList(generics.ListAPIView):
#     queryset = OrderHistory.objects.all()
#     serializer_class = OrderHistorySerializer
#     permission_classes = [IsAuthorPermission]

#     def get_queryset(self):
#         user = self.request.user
#         return OrderHistory.objects.filter(order__user=user).order_by('-order__created_at')

# class OrderHistoryDetail(generics.RetrieveAPIView):
#     queryset = OrderHistory.objects.all()
#     serializer_class = OrderHistorySerializer
#     permission_classes = [IsAuthorPermission]