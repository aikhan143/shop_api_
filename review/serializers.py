from rest_framework import serializers
from .models import *
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.name')

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
            raise serializers.ValidationError('You have rated this post already')
        return product

    def create(self, validated_data):
        user = self.context.get('request').user
        review = Review.objects.create(user=user, **validated_data)
        return review
    
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

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
        like = Like.objects.create(user=user, **validated_data)
        return like
    
class CartProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = '__all__'

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)