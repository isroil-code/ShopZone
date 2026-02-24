from django.contrib import admin
from .models import PromotionToSeller, PromotionToProduct   


@admin.register(PromotionToSeller)
class PromotionToSellerAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'interest', 'start_date', 'end_date', 'code')
    search_fields = ('title', 'seller__user__email', 'code')
    list_filter = ('start_date', 'end_date')
    
@admin.register(PromotionToProduct)
class PromotionToProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'interest', 'start_date', 'end_date', 'code')
    search_fields = ('title', 'product__detail__name', 'code')
    list_filter = ('start_date', 'end_date')
