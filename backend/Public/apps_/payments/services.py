from celery import shared_task
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from decimal import Decimal
from apps_.products.models import Product
from .models import Payment
from apps_.orders.models import Order
from django.db import transaction
from django.utils import timezone
import random
from django.core.mail import send_mail
from .utils import generate_verification_token
from django.conf import settings
from apps_.adminka.models import MoneyInventory
from rest_framework.response import Response


class PaymentAnalyticsService:
     
    @staticmethod
    def get_daily_payments():
        today = timezone.now().date()
        return Payment.objects.filter(created_at__date=today).count() if hasattr(Payment, 'created_at') else 0
    
    
    @staticmethod
    def get_success_vs_failed_payments():
        if hasattr(Payment, 'status') and hasattr(Payment, 'PaymentStatus'):
            success = Payment.objects.filter(status=Payment.PaymentStatus.SUCCESS).count() if hasattr(Payment.PaymentStatus, 'SUCCESS') else 0
            failed = Payment.objects.filter(status=Payment.PaymentStatus.FAILED).count() if hasattr(Payment.PaymentStatus, 'FAILED') else 0
            return {'success': success, 'failed': failed}
        return {'success': 0, 'failed': 0}


    @staticmethod
    def get_weekly_payments():
        week_ago = timezone.now() - timezone.timedelta(days=7)
        return Payment.objects.filter(created_at__gte=week_ago).count() if hasattr(Payment, 'created_at') else 0

    @staticmethod
    def get_total_payments():
        return Payment.objects.count()

    @staticmethod
    def get_canceled_payments():
        return Payment.objects.filter(status=Payment.PaymentStatus.CANCELED).count() if hasattr(Payment, 'status') and hasattr(Payment, 'PaymentStatus') else 0

class FinalPricing:
    
    def get_discounted_price(self, product_price, chegirma, quantity):
        final_base_price = product_price * quantity
        final_discounted_price = int(Decimal(product_price) - chegirma) * quantity
        
        return final_discounted_price, final_base_price
  
    def get_price(self, product_id, quantity):
        if not product_id:
            raise ValidationError('product id kelmadi')
        try:
            product = Product.objects.get(pk=product_id)
            try:
                
                product_price = product.price.price
                chegirma = product.price.chegirma
                if not product_price:
                    return 0, 0
                discounted_price, base_price = self.get_discounted_price(product_price, chegirma, quantity)
                return discounted_price, base_price
            except ObjectDoesNotExist:
                return 0, 0
            
        except Product.DoesNotExist:
            raise ValidationError('bunday product mavjud emas')
        
        

class PaymentService:
    
    
    @staticmethod
    def create_provider_id():
        while True:
            provider_id = f"uz_{random.randint(10000, 99999)}{timezone.now().strftime('%Y%m%d%H%M%S')}"
            if not Payment.objects.filter(provider_payment_id=provider_id).exists():
                return provider_id
    
    @staticmethod
    def create_payment_for_order(order, provider, provider_id=None):
       
            
        if provider == Payment.PaymentProvider.ON_DELIVERY:
            order.status = Order.OrderStatus.CONFIRMING
            order.save(update_fields=['status'])
            try:
                payment = Payment.objects.get(order=order)
            except Payment.DoesNotExist:
                payment = Payment.objects.create(
                    order=order,
                    amount=order.discounted_price,
                    currency='UZS',
                    provider=Payment.PaymentProvider.ON_DELIVERY,
                    status=Payment.PaymentStatus.PENDING,
                    provider_payment_id = provider_id
                )
            payment.status = Payment.PaymentStatus.PROCESSING
            payment.save(update_fields=['status'])
            return {
                'result':{
                    'provider':'on_delivery',
                    'amount': order.discounted_price,
                    'currency': 'UZS',
                    'datail':'Order topshirish punktlariga yetkazib berilganida naqd pulda tulanadai va order status IS_PAID qilinadi'
                    
                }
            }
        
        
        checking_payment = Payment.objects.filter(provider_payment_id=provider_id).first()
        if checking_payment:
            return {
                'result':{
                    'id': checking_payment.provider_payment_id,
                    'order_id': checking_payment.order.pk,
                    'amount': checking_payment.amount,
                    'currency': checking_payment.currency,
                    'provider': checking_payment.provider,
                }
            }

        checking_payment_by_order = Payment.objects.filter(order=order, status=Payment.PaymentStatus.PENDING).first()
        
        if checking_payment_by_order:
            checking_payment_by_order.provider_payment_id = provider_id
            checking_payment_by_order.save(update_fields=['provider_payment_id', 'updated_at'])
            return {
                'result':{
                    'id': checking_payment_by_order.provider_payment_id,
                    'order_id': checking_payment_by_order.order.pk,
                    'amount': checking_payment_by_order.amount,
                    'currency': checking_payment_by_order.currency,
                    'provider': checking_payment_by_order.provider,
                }
            }


        payment = Payment.objects.create(
            order=order,
            amount=order.discounted_price,
            currency='UZS',
            provider=provider,
            status=Payment.PaymentStatus.PENDING,
            provider_payment_id = provider_id
        )

        return {
            'result':{
                'id': payment.provider_payment_id,
                'order_id': payment.order.pk,
                'amount': payment.amount,
                'currency': payment.currency,
                'provider': payment.provider,
            }
        }   

    @transaction.atomic
    def transfer_money(self, payment):
        if payment.status == Payment.PaymentStatus.SUCCESS:
            if hasattr(payment, 'order') and hasattr(payment.order, 'items'):
                for item in payment.order.items.all():
                    product = item.product
                    seller = product.seller
                    MoneyInventory.objects.create(
                        payment_id=payment.provider_payment_id,
                        product_id=product.pk,
                        amount=item.full_price,
                        quantity=item.quantity,
                    )
                return True
        return False

    @staticmethod
    @transaction.atomic
    def handle_provider_callback(provider_payment_id, status):
        try:
            payment = Payment.objects.select_for_update().get(provider_payment_id=provider_payment_id)
        except Payment.DoesNotExist:
            raise ValidationError('payment not found')

        if status == 'success':
            payment.status = Payment.PaymentStatus.SUCCESS
            payment.save(update_fields=['status', 'updated_at'])
            order = payment.order
            order.status = Order.OrderStatus.IS_PAID
            order.save(update_fields=['status'])
            PaymentService().transfer_money(payment)
        elif status in ('failed', 'cancel'):
            payment.status = Payment.PaymentStatus.FAILED
            payment.save(update_fields=['status', 'updated_at'])
        return payment


  
    
    @staticmethod
    def change_status_on_delivery_payment(payment_id):
        try:
            payment = Payment.objects.select_for_update().get(pk=payment_id, provider=Payment.PaymentProvider.ON_DELIVERY)
        except Payment.DoesNotExist:
            raise ValidationError('payment not found')
        
        if payment.status != Payment.PaymentStatus.PROCESSING:
            payment.status = Payment.PaymentStatus.SUCCESS
            payment.save(update_fields=['status', 'updated_at'])
            order = payment.order
            order.status = Order.OrderStatus.IS_PAID
            order.save(update_fields=['status'])
            
            return payment
        return ValidationError('status not valid')
    

    
    
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3},)
def send_verification_link(self, user_id, payment_id):
   
    from apps_.users.models import User
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    token = generate_verification_token(user.id)
    verify_link = f"{settings.NGROK_URL}payment/callback/?token={token}&payment_id={payment_id}"
    send_mail(
        subject='Payment ni verifikatsiya qilish',
        message=f"Payment ni verifikatsiya qilish uchun quyidagi linkni bosing: {verify_link}",
        from_email='isroilberdiyorov3@gmail.com',
        recipient_list=[user.email],
        fail_silently=False,
    )
    
    return token

