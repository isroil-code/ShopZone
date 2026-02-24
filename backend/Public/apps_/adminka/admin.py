from django.contrib import admin
from .models import ECommerceBalance, MoneyInventory

@admin.register(ECommerceBalance)
class ECommerceBalanceAdmin(admin.ModelAdmin):
    list_display = ('id','balance', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(MoneyInventory)
class MoneyInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_id', 'product_id', 'amount', 'quantity', 'status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')