from rest_framework import serializers
from .models import Product, ProductDetail, ProductImages, ProductSertificate, ProductInstruction, ProductPrice, ProductStock, MadeCountry

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["category", 'created_at', 'updated_at']
        
        
    
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = '__all__'
    
    
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "category")

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'
class ProductSertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSertificate
        fields = '__all__'
class ProductInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInstruction
        fields = '__all__'
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = '__all__'
class MadeCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MadeCountry
        fields = '__all__'
    
class ProductSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()
    product_media = serializers.SerializerMethodField()
    product_sertificate = serializers.SerializerMethodField()
    product_instruction = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()
    made_country = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ["category", 'created_at', 'updated_at', 'status','product_detail', 'product_media', 'product_sertificate', 'product_instruction', 'product_price', 'product_stock', 'made_country']

    def get_product_detail(self, obj):
        try:
            data = obj.detail
            return ProductDetailSerializer(data).data
        except ProductDetail.DoesNotExist:
            return None
        
    def get_product_media(self, obj):
        try:
            data = obj.images.all()
            return ProductMediaSerializer(data, many=True).data
        except ProductImages.DoesNotExist:
            return None
        
    def get_product_sertificate(self, obj):
        try:
            data = obj.certificates.all()
            return ProductSertificateSerializer(data, many=True).data
        except ProductSertificate.DoesNotExist:
            return None
        
    def get_product_instruction(self, obj):
        try:
            data = obj.instructions.all()
            return ProductInstructionSerializer(data, many=True).data
        except ProductInstruction.DoesNotExist:
            return None
        
    def get_product_price(self, obj):
        try:
            data = obj.price
            return ProductPriceSerializer(data).data
        except ProductPrice.DoesNotExist:
            return None
        
    def get_product_stock(self, obj):
        try:
            data = obj.stock
            return ProductStockSerializer(data).data
        except ProductStock.DoesNotExist:
            return None
    def get_made_country(self, obj):
        try:
            data = obj.made_countries.all()
            return MadeCountrySerializer(data, many=True).data
        except MadeCountry.DoesNotExist:
            return None
            