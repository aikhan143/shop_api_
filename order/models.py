from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from django.utils.crypto import get_random_string


User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(product.total_price() for product in self.cart_products.all())

    def __str__(self):
        return f"Cart #{self.id} - User: {self.user.name}"

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} - {self.product.title}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='orders', null=True, blank=True, unique=False)
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    payment_link = models.CharField()

    def __str__(self):
        return f"Order #{self.id} with the total price {self.total_price} - User: {self.user.name}."
    
    def create_verification_code(self):
        code = get_random_string(10)
        self.verification_code = code 
        self.save()