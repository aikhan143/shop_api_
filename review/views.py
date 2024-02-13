from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        return super().get_permissions()
    
class CartProductViewSet(ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

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

    def update(self, request):
        product = self.get_object()
        quantity = request.data.get('quantity', None)

        if quantity is not None:
            product.quantity = quantity
            product.save()
            serializer = self.get_serializer(product)
            return Response(serializer.data)

        return Response('Choose an amount', status=400)