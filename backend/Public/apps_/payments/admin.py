from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ('id', 'order', 'amount', 'currency', 'provider', 'status', 'created_at')
	list_filter = ('provider', 'status')
	search_fields = ('provider_payment_id', 'order__order_id')
