from rest_framework import serializers
from .models import *
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.name')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, rating):
        if not rating in range(1, 11):
            raise serializers.ValidationError('Rating can be only from 1 to 10')
        return rating
    
    def validate_product(self, product):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError('You have reviewed this product already')
        return product

    def create(self, validated_data):
        user = self.context.get('request').user
        product_slug = self.context['view'].kwargs.get('slug')

        product = get_object_or_404(Product, slug=product_slug)

        validated_data['product'] = product

        review = Review.objects.create(user=user, **validated_data)
        return review
    
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = Like
        fields = '__all__'

    def validate_product(self, product):
        user = self.context.get('request').user
        if self.Meta.model.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError('You have liked this post already')
        return product    

    def create(self, validated_data):
        user = self.context.get('request').user
        product_slug = self.context['view'].kwargs.get('slug')

        product = get_object_or_404(Product, slug=product_slug)

        validated_data['product'] = product
        like = Like.objects.create(user=user, **validated_data)
        return like
    
class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['products', 'total_price']

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)