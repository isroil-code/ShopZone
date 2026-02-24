from calendar import month
from rest_framework import serializers

from .models import Product, ProductDetail, ProductImages, ProductSertificate, ProductInstruction, ProductPrice, ProductStock, MadeCountry, ProductVideos
from django.utils import timezone
from apps_.reviews.services import ReviewService


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
        return attrs
        
class ProductInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstruction
        fields = ['instruction',]
        
        
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['price','chegirma']
        
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ['quantity', 'quantity_type']
        
        
class MadeCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MadeCountry
        fields = ['country_name',]
        


class CategoryBreadcrumbSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.CharField(max_length=255)    

class OfferSerializer(serializers.Serializer):  
    base_price = serializers.DecimalField(max_digits=30, decimal_places=2)
    discounted_price = serializers.DecimalField(max_digits=30, decimal_places=2)
    final_price = serializers.DecimalField(max_digits=39, decimal_places=2)
    discount_percent = serializers.IntegerField()
    currency = serializers.CharField(max_length=3)
    
    
class IstalledSerializer(serializers.Serializer):
    months = serializers.IntegerField()
    monthly_price = serializers.DecimalField(max_digits=30, decimal_places=2)
    interest = serializers.IntegerField()
    
    
class MediaSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10)
    url = serializers.URLField()
    
class SocialProofSerializer(serializers.Serializer):
    purchases = serializers.IntegerField()
    
class ReviewsSerializer(serializers.Serializer):
     id = serializers.IntegerField()
     user = serializers.CharField(max_length=255)
     rating = serializers.IntegerField()
     afzallik = serializers.CharField(max_length=255)
     kamchilik = serializers.CharField(max_length=255)
     izoh = serializers.CharField(max_length=255)
     created_at = serializers.DateTimeField()
     images = serializers.ListField(child=serializers.URLField())
     
     
class ProductDetailStockSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    quantity_type = serializers.CharField(max_length=50)






class ProductSerialzer(serializers.ModelSerializer):
    detail = ProductDetailSerializer()
    images = ProductImageSerializer(many=True)
    videos = ProductVideosSerializer(many=True)
    certificates = ProductSertificateSerializer(many=True)
    price = ProductPriceSerializer()
    category_name = serializers.CharField(source='category.name', read_only=True)
    reviews = serializers.SerializerMethodField()
    
    
    
    class Meta:
        model = Product
        fields = ["id", "category", "category_name", 'created_at', 'updated_at', 'status', 'detail', 'images', 'videos', 'certificates', 'price', 'reviews']
            
    def get_reviews(self, obj):
        return ReviewService.get_product_reviews_and_rating_count(obj)  
    
class ProductDetailsSerializer(serializers.ModelSerializer):
    detail = ProductDetailSerializer()
    bredcrumbs = CategoryBreadcrumbSerializer(many=True)
    offer = OfferSerializer()
    installments = IstalledSerializer(many=True)
    media = MediaSerializer(many=True)
    certificates = ProductSertificateSerializer(many=True)
    instructions = ProductInstructionSerializer(many=True)
    social_proof = SocialProofSerializer()
    reviews = ReviewsSerializer(many=True)
    stock = ProductDetailStockSerializer()
    
    
    
    class Meta:
        model = Product
        fields = ["id", "category", 'created_at', 'updated_at', 'status','detail', 'media', 'certificates', 'bredcrumbs','instructions', 'offer', 'installments', 'social_proof', 'reviews', 'stock']




