from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
import random
from apps_.products.models import Product
from apps_.users.models import User, Taker


def create_uniqe_order_id():
    running = True  
    while running:
        order_id = random.randint(10000000, 99999999)
        if not Order.objects.filter(order_id=order_id).exists():
            running = False
            return order_id

class Order(models.Model):
        
    class OrderStatus(models.TextChoices):
        PENDING = 'kutilmoqda', 'Kutilmoqda'
        CONFIRMED = 'tasdiqladi', 'Tasdiqlandi'
        CONFIRMING = 'tasdiqlanmoqda', 'Tasdiqlanmoqda'
        IS_PAID = 'to\'lov amalga oshirlidi', 'To\'lov amalga oshirlidi'
        WAITING_FOR_PAYMENT = 'to\'lov kutulmoqda', 'To\'lov kutulmoqda'
        DELIVERING = 'yetkazilmoqda', 'yetkazilmoqda'
        DELIVERED = 'yetkazib berildi', 'Yetkazib berildi'
        CANCELED = 'bekor qilindi', 'Bekor qilindi'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id = models.CharField(max_length=20, default=create_uniqe_order_id)
    status = models.CharField(
        max_length=50, 
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
        
    final_quantity = models.IntegerField(default=1)
    
    base_price = models.DecimalField(
        max_digits=30, 
        decimal_places=2
    )
    discounted_price = models.DecimalField(
        max_digits=30,
        decimal_places=2
    )
   
    
    order_date = models.DateTimeField(auto_now_add=True)
    canceled_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    is_paid_date = models.DateTimeField(null=True, blank=True)
    
    taker = models.ForeignKey(Taker, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    
    
    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()
    full_price = models.DecimalField(max_digits=30, decimal_places=2)
    
    def __str__(self):
        return self.order.order_id
    


class TopshirishPunktlar(models.Model):
    
    class Viloyatlar(models.TextChoices):
        TOSHKENT = 'toshkent', 'Toshkent'
        SAMARQAND = 'samarqand', 'Samarqand'
        BUXORO = 'buxoro', 'Buxoro'
        ANDIJON = 'andijon', 'Andijon'
        FARGONA = 'fargona', 'Farg\'ona'
        NAMANGAN = 'namangan', 'Namangan'
        QASHQADARYO = 'qashqadaryo', 'Qashqadaryo'
        SURXONDARYO = 'surxondaryo', 'Surxondaryo'
        SIRDARYO = 'sirdaryo', 'Sirdaryo'
        JIZZAX = 'jizzax', 'Jizzax'
        NUKUS = 'nukus', 'Nukus'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topshirish_punktlarim')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='topshirish_punkiti')
    
    viloyat = models.CharField(max_length=200, choices=Viloyatlar.choices)
    tuman_or_shahar = models.CharField(max_length=200)
    kucha = models.CharField(max_length=200)
    uy_raqami = models.CharField(max_length=200)
    xonodon = models.CharField(max_length=200)
    pades = models.CharField(max_length=200)
    qavat = models.CharField(max_length=200)
    
    def __str__(self):
        return self.viloyat
    

