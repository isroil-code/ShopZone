from django.shortcuts import render
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializer import (UserProfileSerializer, UserProfileUpdateSerializer,LoginSerializer, VerifySerializer,
                         PasswordForgotSerializer, PasswordSetSerializer, ChangePassword, LogoutSerializer)
from rest_framework import permissions as p
from .services import send_otp, send_recovery_otp
from django.core.cache import cache
from django.db import transaction
from .models import UserProfile
from rest_framework.generics import ListAPIView
from config.permissions import IsCustomer, IsAdmin
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from apps_.cart.services import create_cart
from rest_framework import status

class LoginView(GenericAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serilizer = self.serializer_class(data=request.data)
        serilizer.is_valid(raise_exception=True)
        email = serilizer.validated_data['email']
        password = serilizer.validated_data['password']
        if not email or not password:
            return Response({'detail':"email and passwrd are required!!!"}, status=400)
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_verified:
                refresh = RefreshToken.for_user(user=user)
                return Response({
                    'detail': 'Logged in successfully',
                    'access': str(refresh.access_token), 
                    'refresh': str(refresh),
                    'user': {   
                        'user_id': user.id,
                        'email': user.email,
                    },
                    'redirect_to':'home, main page'
                }, status=status.HTTP_200_OK)
            else:
                send_otp.delay(email)
                return Response({'detail': 'User not verified. OTP sent again.',
                                 'is_verified': user.is_verified}, status=status.HTTP_200_OK)
        else:
            if User.objects.filter(email=email).exists():
                return Response({'detail': 'Password or Email is wrong!!!'}, status=status.HTTP_400_BAD_REQUEST)
            User.objects.create_user(email=email, password=password)
            send_otp.delay(email)
            return Response({'detail': 'User Created. OTP code sent', 'is_verified': False}, status=status.HTTP_201_CREATED)
        
        
class VerifyView(GenericAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = VerifySerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user_code = serializer.validated_data['code']
        
        if not email or not user_code:
            return Response({'detail':"email and code are required!!!"}, status=400)
        
        user = User.objects.filter(email=email).first()
        code = cache.get(f'{email}_code', None)
        
        if user.is_verified:
            return Response({'detail':'you already verified!!'}, status=200)
        
        if user and str(user_code) == str(code):
            with transaction.atomic():
                user.is_verified = True
                user.save(update_fields=['is_verified'])
                refresh = RefreshToken.for_user(user=user)
                cache.delete(f'{email}_code')
                UserProfile.objects.get_or_create(user=user)
                create_cart(user=user)
            return Response({'detail': 'Logged in successfully', 'access': str(refresh.access_token), 'refresh': str(refresh)}, status=200)
        return Response({'detail':'code is wrong. Try again!!!'})
    
    
class ForgotPasswordView(GenericAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = PasswordForgotSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        if user:
            send_recovery_otp.delay(email)
            return Response({'detail':'recovery otp sent'}, status=200)
        return Response({'detail':'Email not found'}, status=400)            

class VerifyRecoveryOtpView(GenericAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = VerifySerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user_code = serializer.validated_data['code']
        
        code = cache.get(f'{email}_recovery', None)
        if str(user_code) == str(code):
            return Response({'detail':'set new password'}, status=200)
        return Response({'detail':'error'}, status=400)
    

class SetPasswordView(GenericAPIView):
    permission_classes = [p.AllowAny]
    serializer_class = PasswordSetSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password1 = serializer.validated_data['password1']
        password2 = serializer.validated_data['password2']
        
        user = User.objects.get(email=email)
        if user and str(password1) == str(password2):
            user.set_password(password1)
            user.save(update_fields=['password'])
            return Response({'detail':'password set sucessfully'}, status=200)
        return Response({'detail':'something went wrong'}, status=400)
        
    
class ChangePasswordView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = ChangePassword
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = User.objects.get(email=request.user.email)
        recent_password = serializer.validated_data['recent_password']
    
        password1 = serializer.validated_data['password1']
        password2 = serializer.validated_data['password2']
        
        password_check = authenticate(request, email=user.email, password=recent_password)
        if password_check:
            if user and str(password1) == str(password2):
                user.set_password(password1)
                user.save(update_fields=['password'])
                return Response({'detail':'password set sucessfully'}, status=200)
            return Response({'detail':'something went wrong'}, status=400)
        return Response({'detail':'Recent password is wrong'}, status=400)
        

class LogoutView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]
    serializer_class = LogoutSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            refresh = request.data['refresh_token']
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({'detail':'Logged out successfully'}, status=200)
        except:
            return Response({'detail':'something went wrong!!'}, status=400)

class UserProfileView(GenericAPIView):
    permission_classes = [p.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserProfileSerializer
        return UserProfileUpdateSerializer

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=200)

    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

        
        



class UsersListAdmin(ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    http_method_names = ['get', 'put', 'delete']
    
    @action(detail=True, methods=['put'], permission_classes=[IsAdmin])
    def block(self, request, pk=None):
        with transaction.atomic():
            user_profile = self.get_object()
            user_profile.user.is_blocked = True
            user_profile.user.save(update_fields=['is_blocked'])
            return Response({'detail':'user blocked'}, status=200)
        return Response({'detail':'user not blocked'}, status=400)
        
    
    @action(detail=True, methods=['put'], permission_classes=[IsAdmin])
    def un_block(self, request, pk=None):
        with transaction.atomic():
            user_profile = self.get_object()
            user_profile.user.is_blocked = False
            user_profile.user.save(update_fields=['is_blocked'])
            return Response({'detail':'user unblocked'}, status=200)
        return Response({'detail':'user not unblocked'}, status=200)
    
    

    
    

    


