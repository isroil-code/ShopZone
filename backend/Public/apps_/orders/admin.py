from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'user', 'status', 'final_quantity', 'base_price', 'discounted_price']
    search_fields = ['order_id', 'user__email']
    list_filter = ['status']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'full_price']
    search_fields = ['order__order_id', 'product__name']
    
    