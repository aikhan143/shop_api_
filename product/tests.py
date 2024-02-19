from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model
from .views import *
from django.test import TestCase
from product.models import Brand, Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(title='cat')
        self.user = User.objects.create_user(email='test@gmail.com', password='12345678', name='a', is_active=True)
        self.brand = Brand.objects.create(user=self.user, title='brand')

        products = [
            Product(
                title = 'prod',
                description = 'desc',
                category = self.category,
                price = 12,
                brand = self.brand,
                slug = '1'
            ),
            Product(
                title = 'prod2',
                description = 'desc',
                category = self.category,
                price = 12,
                brand = self.brand,
                slug = '2'
            )
        ]
        Product.objects.bulk_create(products)

    def test_create(self):
        data = {
            'title': 'prod1',
            'description': '12',
            'category': CategorySerializer(self.category).data,
            'price': 12,
            'brand': BrandSerializer(self.brand).data,
        }

        request = self.factory.post('/api/v1/products/', data, format='json')
        view = ProductViewSet.as_view({'post': 'create'})
        response = view(request)
        assert Product.objects.filter(title=data['title']).exists()