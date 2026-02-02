from rest_framework import serializers
from .models import Product, ProductDetail, ProductImages, ProductSertificate, ProductInstruction, ProductPrice, ProductStock, MadeCountry, ProductVideos
from django.utils import timezone


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["category", 'created_at', 'updated_at']
        
    
    
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = [ 'name', 'short_description', 'full_description']
        
    def validate(self, attrs):
        if len(attrs['full_description']) < 30:
            raise serializers.ValidationError("Full description must be at least 30 characters long.")
        return attrs
    
    
    
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id",)

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImages
        fields = ['image']
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return f"http://127.0.0.1:8000{obj.image.url}"
        return None
        
    def validate_image(self, value):
        if value.size > 10 * 1024 * 1024:  
            raise serializers.ValidationError("Image size should not exceed 10MB.")
        
        if value.image.width < 800 or value.image.height < 600:
            raise serializers.ValidationError("Image resolution should be at least 800x600 pixels.")
        return value
    
    
class ProductVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideos
        fields = ['video',]
        
    def validate_video(self, value):
        if value.size > 20 * 1024 * 1024:  
            raise serializers.ValidationError("Video size should not exceed 20MB.")
        
        if not value.name.endswith(('.mp4', '.avi', '.mov')):
            raise serializers.ValidationError("Unsupported video format. Allowed formats: mp4, avi, mov.")
        return value
        
class ProductSertificateSerializer(serializers.ModelSerializer):
    sertificate_image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductSertificate
        fields = ['sertificate_image', 'sertificate_number', 'sertificate_expiry_date']
    
    def get_sertificate_image(self, obj):
        request = self.context.get('request')
        if obj.sertificate_image and hasattr(obj.sertificate_image, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.sertificate_image.url)
            return f"http://127.0.0.1:8000{obj.sertificate_image.url}"
        return None
        
    def validate(self, attrs):
        if attrs['sertificate_expiry_date'] < timezone.now().date():
            raise serializers.ValidationError("Expire date of the sertificate already expired.")
        
class ProductInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstruction
        fields = ['instruction',]
        
        
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['price', 'discount_price']
        
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ['quantity', 'reserved_quantity']
        
        
class MadeCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MadeCountry
        fields = ['country_name',]
    
class ProductSerializer(serializers.ModelSerializer):
    detail = ProductDetailSerializer()
    images = ProductImageSerializer(many=True)
    videos = ProductVideosSerializer(many=True) 
    certificates = ProductSertificateSerializer(many=True)
    instructions = ProductInstructionSerializer(many=True)
    price = ProductPriceSerializer()    
    stock = ProductStockSerializer()
    made_countries = MadeCountrySerializer(many=True)
    
    class Meta:
        model = Product
        fields = ["id", "category", 'created_at', 'updated_at', 'status','detail', 'images','videos', 'certificates', 'instructions', 'price', 'stock', 'made_countries']



