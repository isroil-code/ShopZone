from rest_framework import serializers
from .models import Order, OrderItem
from apps_.payments.serializer import TakerSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_short_description = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'full_price', 'product_images', 'product_name', 'product_short_description']
        
    def get_product_images(self, obj):
        try:
            images = obj.product.images.all()
            return [image.image.url for image in images]
        except obj.product.images.RelatedObjectDoesNotExist:
            return []
    
    def get_product_name(self, obj):
        try:
            return obj.product.detail.name
        except obj.product.detail.RelatedObjectDoesNotExist:
            return 
        
    def get_product_short_description(self, obj):
        try:
            return obj.product.detail.short_description
        except obj.product.detail.RelatedObjectDoesNotExist:
            return

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    taker = TakerSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'order_id', 'status', 'final_quantity', 'base_price','taker', 'discounted_price', 'items']
        
