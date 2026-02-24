from django.core.exceptions import ValidationError
import string
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
from django.core.mail import send_mail
import random
from django.core.cache import cache
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken



@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_otp(email):
    code = random.randint(10000,99999)
    cache.set(f'{email}_code', code, timeout=60 * 5)

    send_mail(
            subject='Salom!',
            message=f'Tasdiqlash Kodi: {code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    
    return code
    
    
    
class SellerService:
    
    @staticmethod
    @transaction.atomic
    def create_seller():
        pass
    
    @staticmethod
    def generate_jwt_token(seller):
        if not seller and not seller.is_verified:
            return ValidationError('Seller object verifikatsiya qilinmagan')
        
        refresh = RefreshToken.for_user(user=seller)
        data = {
            'access':str(refresh.access_token), 
            'refresh':str(refresh),
            'seller':{
                'id':seller.id,
                'email':seller.email,
                'status':seller.status
            }
        }
        return data
    