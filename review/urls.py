from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('comments', ReviewViewSet)
router.register('like', LikeViewSet)
router.register('cart', CartProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/<slug:slug>/add_to_cart/', CartProductViewSet.as_view({'post': 'add_to_cart'}), name='cart-add-to-cart'),
    path('products/<slug:slug>/like/', LikeViewSet.as_view({'post': 'create'}), name='like-create'),
    path('products/<slug:slug>/dislike/', LikeViewSet.as_view({'delete': 'destroy'}), name='like-destroy')
]