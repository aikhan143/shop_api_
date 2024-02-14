from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from product.permissions import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
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
    
# class CartProductViewSet(ModelViewSet):
#     queryset = CartProduct.objects.all()
#     serializer_class = CartProductSerializer
#     permission_classes = [IsAuthenticated]

#     def update(self, request):
#         product = self.get_object()
#         quantity = request.data.get('quantity', None)

#         if quantity is not None:
#             product.quantity = quantity
#             product.save()
#             serializer = self.get_serializer(product)
#             return Response(serializer.data)

#         return Response('Choose an amount', status=400)

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthorPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(user=user).order_by('created_at')
        return queryset
    
    def destroy(self, request):
        instance = self.get_object()
        instance.is_completed = True  
        instance.save()
        return Response("Order completed successfully", status=204)
    
class VerificationCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = VerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.verify()
        return Response('Verification successful', status=200)