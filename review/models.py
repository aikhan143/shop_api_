from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from django.db.models.signals import post_save

User = get_user_model()

class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} - {self.comment}'

class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user} liked {self.product}'
    
class Cart(models.Model):
    products = models.ManyToManyField(Product, through='CartProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(product.total_price() for product in self.cart_products.all())

    def __str__(self):
        return f"Cart #{self.id} - User: {self.user.username}"

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} - {self.product.title}"

