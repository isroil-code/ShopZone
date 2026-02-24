from django.db import models
from apps_.users.models import User
from apps_.orders.models import Order
from django.conf import settings
import random

class Payment(models.Model):
    
    class PaymentProvider(models.TextChoices):
        PAYME = "payme", "Payme"
        CLICK = "click", "Click"
        STRIPE = "stripe", "Stripe"
        PAYPAL = "paypal", "PayPal"
        ON_DELIVERY = "on_delivery", "Yetkazib berishda to'lash"
    
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        CANCELED = "canceled", "Canceled"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=30, decimal_places=2)
    currency = models.CharField(max_length=10, default="UZS")

    provider = models.CharField(max_length=50, choices=PaymentProvider.choices)  
    provider_payment_id = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomClick(models.Model):
        pass