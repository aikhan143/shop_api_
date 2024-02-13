from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from review.models import Cart

User = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
