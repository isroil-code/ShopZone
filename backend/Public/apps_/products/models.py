from django.db import models
from apps_.categories.models import Category
from apps_.sellers.models import Seller
from apps_.users.models import User
from django.core.exceptions import ValidationError

class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        MODERATION = 'moderation', 'Moderation'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
    
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='products')
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def get_media(self, request):
        media = []
        if self.images:
            for image in self.images.all():
                media.append({
                    'type':'image', 
                    'url':f'{request.build_absolute_uri(image.image.url)}'
                })
        if self.videos:
            for video in self.videos.all():
                media.append({
                    'type':'video',
                    'url':f'{request.build_absolute_uri(video.video.url)}'
                })
        return media
    
    def get_stock(self):
        try:
            return {'quantity': self.stock.quantity, 'quantity_type': self.stock.quantity_type}
        except ProductStock.DoesNotExist:
            return {'quantity': 0, 'quantity_type': None}
    
    def __str__(self):
        return self.seller.user.email + " - " + self.detail.name if hasattr(self, 'detail') else "Unnamed Product"
    
class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='detail')
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    full_description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.seller.user.email} - {self.name}"
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f" {self.product.seller.user.email} - {self.product.detail.name}"
    

class ProductVideos(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='product_videos/')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.seller.user.email} - {self.product.detail.name}"    

class ProductSertificate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='certificates')
    sertificate_image = models.ImageField(upload_to='product_certificates/')
    sertificate_number = models.CharField(max_length=255)   
    sertificate_expiry_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" {self.product.seller.user.email} - {self.product.detail.name}"
    
class ProductInstruction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='instructions')
    instruction = models.TextField(null=True, blank=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.seller.user.email} - {self.product.detail.name}"
    
class ProductPrice(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='price')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Asosiy narx uzbek sumida')
    chegirma = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,  help_text='Chegirma price - chegirms = sotiladigan summa')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" {self.product.seller.user.email} - {self.product.detail.name}"
    
        
    
    
class ProductStock(models.Model):
    class QuantityTypes(models.TextChoices):
        KG = 'kilogram', 'Kilogram'
        DONA = 'dona', 'Dona'
        METR = 'metr', 'Metr'
        OTHER = 'other', 'Other'
        
        
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField()
    quantity_type = models.CharField(max_length=50, choices=QuantityTypes.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.seller.user.email} - {self.product.detail.name}"

class MadeCountry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='made_countries')
    country_name = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.seller.user.email} - {self.country_name}"    
    
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

    color = models.CharField(max_length=50, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.seller.user.email} - {self.variant_name}"
    
# class ProductOrders(models.Model):
#     class ProductOrderStatus(models.TextChoices):
#         NOT_PAID = 'tulanmagan', 'Tulanmagan'
#         PAID = 'tulandi', 'Tulandi'
#         DELIVERING = 'yetkazib berilmoqda', 'Yetkazib berilmoqda'
#         DELIVERED = 'yetkazib berild', 'Yetkazib berildi'
        
#     product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
#     buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='my_orders')
    



    



