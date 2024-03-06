from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from product.permissions import *
from rest_framework.response import Response

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
