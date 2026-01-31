from django.db import models
from apps_.categories.models import Category
from apps_.sellers.models import Seller

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
    
    
    def __str__(self):
        return self.seller.user.email + " - Product"
    
class ProductDetail(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='detail')
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    full_description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Detail of {self.product.seller.user.email} - {self.name}"
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    video = models.FileField(upload_to='product_videos/', null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Image for {self.product.seller.user.email} - {self.product.detail.name}"
    
class ProductSertificate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='certificates')
    sertificate_image = models.ImageField(upload_to='product_certificates/')
    sertificate_number = models.CharField(max_length=255)   
    sertificate_expiry_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Certificate for {self.product.seller.user.email} - {self.product.detail.name}"
    
class ProductInstruction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='instructions')
    instruction = models.TextField(null=True, blank=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Instruction for {self.product.seller.user.email} - {self.product.detail.name}"
    
class ProductPrice(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='price')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Asosiy narx uzbek sumida')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Price for {self.product.seller.user.email} - {self.product.detail.name}"
    
    
class ProductStock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField()
    reserved_quantity = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stock for {self.product.seller.user.email} - {self.product.detail.name}"

class MadeCountry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='made_countries')
    country_name = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Made Country for {self.product.seller.user.email} - {self.country_name}"

    


