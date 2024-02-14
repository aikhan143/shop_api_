from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()

class Brand(models.Model):
    slug = models.SlugField(max_length=100,primary_key=True, blank=True)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brands')
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()
    
class Category(models.Model):
    slug = models.SlugField(max_length=100,primary_key=True, blank=True)
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class Product(models.Model):
    slug = models.SlugField(max_length=100,primary_key=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_img/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()