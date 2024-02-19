from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model
from .views import *

User = get_user_model()

class UserTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='user@gmail.com',
            password='123456789',
            is_active=True,
            activation_code=1234,
        )

    def test_registration(self):
        data = {
            'email': 'user@gmail.com',
            'password': '123456789',
            'password_confirm': '123456789',
            'name': 'danysh',
            'brand': 'somebrand',
            'is_brand': 'True'
        }
        request = self.factory.post('/api/v1/account/register/', data, format='json')
        view = RegistrationView.as_view()
        response = view(request)
        print(response.status_code)
        assert User.objects.filter(email=data['email']).exists()

    def test_login(self):
        data = {
            'email': 'user@gmail.com',
            'password': '123456789'
        }
        request = self.factory.post('login/', data=data, format='json')
        view = LoginView.as_view()
        response = view(request)
        assert 'token' in response.data

