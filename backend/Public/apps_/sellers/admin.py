from django.contrib import admin
from .models import Seller, SellerProfile, SellerIndividual, SellerEntrepreneur, SellerCompany, SellerBankAccount, Shartnoma, SellerBalance

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'biznes_type', 'status', 'created_at', 'updated_at')
    search_fields = ('biznes_type', 'status')
    list_filter = ('status', 'created_at')
    
@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin): 
    list_display = ('id', 'seller', 'name', 'surname', 'phone_number2', 'father_name')
    search_fields = ('name', 'surname', 'phone_number2')    
    
    
@admin.register(SellerIndividual)
class SellerIndividualAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'jshshir', 'ruyhatdan_otish_guvohnamasi_raqami', 'created_at', 'updated_at')
    search_fields = ('jshshir', 'ruyhatdan_otish_guvohnamasi_raqami')
    
@admin.register(SellerEntrepreneur)
class SellerEntrepreneurAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'jshshir', 'ruyhatdan_otish_guvohnamasi_raqami', 'created_at')
    search_fields = ('jshshir', 'ruyhatdan_otish_guvohnamasi_raqami')
    
@admin.register(SellerCompany)
class SellerCompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'company_name', 'stir', 'oked', 'created_at', 'updated_at')
    search_fields = ('company_name', 'stir', 'oked')
    
@admin.register(SellerBankAccount)
class SellerBankAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'bank_name', 'account_number', 'created_at', 'updated_at')
    search_fields = ('bank_name', 'account_number')
    
@admin.register(Shartnoma)
class ShartnomaAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'created_at', 'updated_at')
    search_fields = ('seller__user__email',)
    
@admin.register(SellerBalance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'amount', 'available_amount')
    search_fields = ('seller__user__email',)
    