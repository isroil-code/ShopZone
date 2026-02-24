from django.shortcuts import render
from .serializer import *
from rest_framework import generics, permissions
from .models import Seller
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from . services import send_otp, SellerService


class RegisterSellerView(generics.CreateAPIView):
    serializer_class = RegisterSellerSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        email = serializer.validated_data['email']
        if email:
            otp = send_otp.delay(email)
            return Response({'detail': 'OTP sent to email', 'code':str(otp)}, status=status.HTTP_201_CREATED)
        raise Response({'detail':'error'}, status=status.HTTP_400_BAD_REQUEST)
        
        
    
class LoginSellerView(generics.GenericAPIView):
    serializer_class = LoginSellerSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        service = SellerService()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        seller = authenticate(request, email=email, password=password)
        if seller is not None:
            if not seller.is_verified:
                return Response({'detail': 'Account not verified'}, status=status.HTTP_403_FORBIDDEN)
            token = service.generate_jwt_token(seller=seller)
            return Response({'detail': token}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class VerifySellerView(generics.GenericAPIView):
    serializer_class = VerifySellerSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        service = SellerService()
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user_code = serializer.validated_data['code']
        
        try:
            cached_code = cache.get(f'{email}_code')
            if cached_code and str(cached_code) == str(user_code):
                seller = Seller.objects.get(email=email)
                seller.is_verified = True
                seller.save(update_fields=['is_verified'])
                token = service.generate_jwt_token(seller=seller)
                return Response({'detail': token}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)
        except Seller.DoesNotExist:
            return Response({'detail': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    