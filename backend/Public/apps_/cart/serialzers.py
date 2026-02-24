from rest_framework import serializers
from .models import CartItem, Cart, Wishlist, WishlistItems
from decimal import Decimal
from apps_.products.models import ProductPrice
from apps_.payments.services import FinalPricing
from .services import calculate_cart_total

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(
        source='product.id',
        read_only=True
    )

    product_price = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_id', 'product_price', 'quantity', 'final_price', 'created_at', 'updated_at','is_selected'
        ]

    def get_product(self, obj):
        try:
            return obj.product.detail.name
        except obj.product.detail.RelatedObjectDoesNotExist:
            return "Noma'lum mahsulot"

    def get_product_price(self, obj):
        try:
            return obj.product.price.price
        except ProductPrice.DoesNotExist:
            return None

    def get_final_price(self, obj):
        try:
            return (obj.product.price.price - obj.product.price.chegirma) * Decimal(obj.quantity)
        except ProductPrice.DoesNotExist:
            return None
        
class CartSerialzier(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    final_prices = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['user', 'created_at', "items", "final_prices"]
        
    def get_final_prices(self, obj):
        return calculate_cart_total(obj)
        
    
class WishListItemSerialzier(serializers.ModelSerializer):
    class Meta:
        model = WishlistItems
        fields = '__all__'
        
class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerialzier(many=True)
    
    class Meta:
        model = Wishlist
        fields = ['user', 'created_at', 'items']