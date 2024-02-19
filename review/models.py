from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

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
    product = models.ForeignKey(Product, on_delete=models .CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user} liked {self.product}'
    
