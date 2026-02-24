from rest_framework import serializers
from .models import PromotionToProduct, PromotionToSeller

class PromotionToSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionToSeller
        fields = '__all__'
        read_only_fields = ['seller', 'created_at', 'updated_at']

class PromotionToProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionToProduct
        fields = '__all__'
        read_only_fields = ['product', 'created_at', 'updated_at']
        
        
        