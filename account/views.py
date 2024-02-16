from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
import logging
from . import tasks

class RegistrationView(APIView):

    @swagger_auto_schema(request_body=RegistrationSerializer())
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            'Account has been successfully created', status=201
        )


class ActivationView(APIView):

    @swagger_auto_schema(request_body=ActivationSerializer())
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response(
                'User has been activated',
                status=200
            )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
      
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()

        return Response('You have successfully logged out')
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password has been changed', status=200)
    
class ForgotPasswordView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.send_verification_email()
        return Response('Password recovery code has been sent to your email', status=200)
    
class ForgotPasswordCompleteView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer())
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password has been changed', status=200)
    

 


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch') 
class TestView(View):
    def get(self, request):
        try:
            example_instance = {'username': 'test_user', 'email': 'test@example.com'}
            serializer = AccountSerializer(data=example_instance)
            if serializer.is_valid():
                return JsonResponse(serializer.data)
            else:
                return JsonResponse({'errors': serializer.errors}, status=400)
        except Exception as e:
            logger.error("Произошла ошибка в TestView: %s", str(e))
   
            