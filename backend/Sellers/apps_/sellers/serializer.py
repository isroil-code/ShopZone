from rest_framework import serializers
from .models import Seller, SellerIndividual, SellerEntrepreneur, SellerCompany, Shartnoma, SellerBalance


class RegisterSellerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = Seller
        fields = ['name', 'biznes_type', 'phone', 'email', 'password']
    
    def create(self, validated_data):
        seller = Seller.objects.create_user(
            email=validated_data['email'],  
            password=validated_data['password'],
            name=validated_data['name'],
            biznes_type=validated_data['biznes_type'],
            phone=validated_data['phone']
        )
        return seller
    
class LoginSellerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
class VerifySellerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)