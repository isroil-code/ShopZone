from rest_framework import serializers
from .models import UserProfile, User
from rest_framework.response import Response
from .services import send_recovery_otp
from .models import Taker


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    role = serializers.CharField(source='user.role')
    is_verified = serializers.CharField(source='user.is_verified')
    is_blocked = serializers.CharField(source='user.is_blocked')
    class Meta:
        model = UserProfile
        fields = ('id','name', 'surname', "father_name", 'birthday', 'gender', 'phone', 'email', 'role', 'is_verified', 'is_blocked')
        
        
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    class Meta:
        model = UserProfile
        fields = ('name', 'surname', "father_name", 'birthday', 'gender', 'phone')
        

class PasswordForgotSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  
    

class PasswordSetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    
    
class ChangePassword(serializers.Serializer):
    recent_password = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    
    
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    
    
    
