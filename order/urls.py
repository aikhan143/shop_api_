from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('products/<slug:pk>/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='cart-add-to-cart'),
    path('order/verify-order/<int:pk>/', VerificationViewSet.as_view({'post': 'create'})),
    # path('order-history/', OrderHistoryList.as_view(), name='order-history-list'),
    # path('order-history/<int:pk>/', OrderHistoryDetail.as_view(), name='order-history-detail'),
    ]

urlpatterns += router.urls