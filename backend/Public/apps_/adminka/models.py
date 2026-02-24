from django.db import models

class ECommerceBalance(models.Model):
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"ECommerce Balance: {self.balance}"
    
    
class MoneyInventory(models.Model):
    class Status(models.TextChoices):
        TRANSFERED_SELLER = 'TRANSFERED_SELLER', 'Transfered to Seller'
        PENDING = 'PENDING', 'Pending'
    
    payment_id = models.CharField(max_length=100, unique=True)
    product_id = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    quantity = models.PositiveIntegerField()
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return f"{self.product_id}: {self.amount} {self.status}"


