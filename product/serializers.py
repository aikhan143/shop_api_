from rest_framework.serializers import ReadOnlyField, ModelSerializer, ValidationError
from .models import *
from django.contrib.auth import get_user_model
from review.serializers import *
from review.models import *
from django.db.models import Avg

User = get_user_model()

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_brand(self, brand):
        if not User.objects.filter(brand=brand).exists():
            raise ValidationError('You have no access to this brand.')
        return brand
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['reviews'] = ReviewSerializer(Review.objects.filter(product=instance.pk), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']

        return representation
    
class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'image', 'price']
        
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = ProductSerializer(Product.objects.filter(category=instance.pk), many=True).data
        return representation

class BrandSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.name')
    class Meta:
        model = Brand
        fields = ['title', 'products']

    def create(self, validated_data):
        user = self.context.get('request').user
        brand = Brand.objects.create(user=user, **validated_data)
        return brand
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = ProductSerializer(Product.objects.filter(brand=instance.pk), many=True).data
        return representation
