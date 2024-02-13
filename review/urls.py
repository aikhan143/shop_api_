from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<slug:pk>/add_to_cart/', CartViewSet.as_view({'post': 'add_to_cart'}), name='cart-add-to-cart'),
    path('products/<slug:slug>/like/', LikeViewSet.as_view({'post': 'create'}), name='like-create'),
    path('products/<slug:slug>/dislike/', LikeViewSet.as_view({'delete': 'destroy'}), name='like-destroy'),
    path('products/<slug:slug>/reviews/', ReviewViewSet.as_view({'post': 'create', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='review-create')
]