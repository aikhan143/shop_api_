from django.urls import path, include
from .views import *


urlpatterns = [
    path('products/<slug:slug>/like/', LikeViewSet.as_view({'post': 'create'}), name='like-create'),
    path('products/<slug:slug>/dislike/', LikeViewSet.as_view({'delete': 'destroy'}), name='like-destroy'),
    path('products/<slug:slug>/reviews/', ReviewViewSet.as_view({'post': 'create', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='review-create')
]