from django.contrib import admin
from .models import *

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_verified', 'created_at')
    
