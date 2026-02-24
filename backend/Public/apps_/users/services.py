from django.db import transaction
from django.core.mail import send_mail
import random
from django.core.cache import cache
from django.conf import settings
from django.db import transaction
from .models import UserProfile
import string

from django.utils import timezone
from .models import User


class UserAnalyticsService:
    @staticmethod
    def get_daily_registrations():
        today = timezone.now().date()
        return User.objects.filter(created_at__date=today).count()

    @staticmethod
    def get_weekly_registrations():
        week_ago = timezone.now() - timezone.timedelta(days=7)
        return User.objects.filter(created_at__gte=week_ago).count()

    @staticmethod
    def get_total_users():
        return User.objects.count()

    @staticmethod
    def get_active_users_dau():
        today = timezone.now().date()
        return User.objects.filter(last_login__date=today).count()

    @staticmethod
    def get_active_users_mau():
        month_ago = timezone.now() - timezone.timedelta(days=30)
        return User.objects.filter(last_login__gte=month_ago).count()

    @staticmethod
    def get_blocked_users():
        return User.objects.filter(is_blocked=True).count()


# from celery import shared_task
from django.core.mail import send_mail



# @shared_task(
#     autoretry_for=(Exception,),
#     retry_backoff=True,
#     retry_kwargs={"max_retries": 3},
# )
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
    
    
    
# @shared_task(
#     autoretry_for=(Exception,),
#     retry_backoff=True,
#     retry_kwargs={"max_retries": 3},
# )
def send_recovery_otp(email):
    code = random.choices(string.ascii_uppercase, k=6)
    code_1 = ''
    for i in code:
        code_1 += i
    cache.set(f'{email}_recovery', code_1, timeout=60 * 5)

    send_mail(
            subject='Salom!',
            message=f'Tasdiqlash Kodi: {code_1}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    
    
