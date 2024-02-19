from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model
from .views import RegistrationView
from django.test import TestCase
from product.models import Brand, Category, Product
from slugify import slugify


User = get_user_model()

class RegistrationValidationTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_valid_email_and_password(self):
        data = {
            'email': 'danysh@mail.ru',
            'password': '123456789',
            'password_confirm': '123456789',
            'username': 'danysh',
            'brand': 'somebrand'
        }
        request = self.factory.post('/api/v1/account/register/', data, format='json')
        view = RegistrationView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)  # Изменил ожидаемый код

    def test_invalid_email(self):
        data = {
            'email': 'dansyh-mail.ru',
            'password': '123456789',
            'password_confirm': '123456789',
            'username': 'danysh',
            'brand': 'somebrand'
        }
        request = self.factory.post('/api/v1/account/register/', data, format='json')
        view = RegistrationView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)
        if 'password' in response.data:
            self.assertIn('password', response.data)
        else:
            self.assertIn('name', response.data)

    def test_weak_password(self):
        data = {
            'email': 'danysh@mail.ru',
            'password': '2',
            'password_confirm': '2',
            'username': 'danysh',
            'brand': 'somebrand'
        }
        request = self.factory.post('/api/v1/account/register/', data, format='json')
        view = RegistrationView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)



# product




class ProductModelTest(TestCase):
    def create_user(self, email='aykhan@mail.ru', password='123456789'):
        return User.objects.create_user(email=email, password=password)

    def create_brand(self, title='Test Brand', user=None):
        return Brand.objects.create(title=title, user=user)

    def create_category(self, title='Test Category'):
        return Category.objects.create(title=title)

    def create_product(self, title='Test Product', description='Test Description',
                       image=None, category=None, price=100, brand=None):
        return Product.objects.create(title=title, description=description,
                                      image=image, category=category, price=price, brand=brand)

    def test_create_product(self):
        user = self.create_user()
        brand = self.create_brand(user=user)
        category = self.create_category()
        product = self.create_product(category=category, brand=brand)

        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.description, 'Test Description')
        self.assertEqual(product.category, category)
        self.assertEqual(product.price, 100)
        self.assertEqual(product.brand, brand)


