from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from apps_.sellers.models import Seller
from apps_.products.models import Product
from apps_.users.models import User



class PromotionToSeller(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='promotions')
    title = models.CharField(max_length=255)
    interest = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()   
    
    code = models.CharField(max_length=50, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.seller.user.email}"
    
class PromotionToProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotions')
    title = models.CharField(max_length=255)
    interest = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()   
    
    code = models.CharField(max_length=50, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.product.detail.name}"
    
    
class UserUsedPromotion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='used_promotions')
    promotion_id = models.PositiveIntegerField()
    promotion_type = models.CharField(max_length=20) 
    used_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.promotion_type} - {self.promotion_id}"
    
    
    