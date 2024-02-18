from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('brands', BrandViewSet)

urlpatterns = [
    path('recommend-products/', ProductRecommendationView.as_view()),

    path('', include(router.urls)),
]