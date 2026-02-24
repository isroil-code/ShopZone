from django.db import models
from apps_.users.models import User
from .validators import validate_file, validate_account_number
import random
from django.utils import timezone
from datetime import timedelta



class Seller(models.Model):
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        REVIEW = 'review', 'Review'
        VERIFIED = 'verified', 'Verified'
        REJECTED = 'rejected', 'Rejected'
        BLOCKED = 'blocked', 'Blocked'
    
    class BusinessType(models.TextChoices):
        INDIVIDUAL = 'individual', 'Yakka tartibdagi tadbirkor'
        ENTREPRENEUR = 'entrepreneur', 'O\'zini o\'zi band qilgan shaxs'
        COMPANY = 'company', 'MChJ yoki boshqa yuridik shaxs'
    
    user = models.OneToOneField(User,
                                 on_delete=models.CASCADE, 
                                 related_name='seller')
    
    biznes_type = models.CharField(max_length=50, choices=BusinessType.choices, null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers' 
        indexes = [
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - Seller"
    
    
class SellerProfile(models.Model):
    seller = models.OneToOneField(Seller, 
                                  on_delete=models.CASCADE, 
                                  related_name='profile')
    
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number2 = models.CharField(max_length=20, help_text='qushimcha telefon raqam')
    father_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Information for {self.seller.user.email} {self.name}"
    
    
class SellerIndividual(models.Model):
    seller = models.OneToOneField(Seller, 
                                  on_delete=models.CASCADE, 
                                  related_name='individual_info')
    
    jshshir = models.CharField(max_length=14, unique=True, help_text='JSHSHIR raqami')
    ruyhatdan_otish_guvohnamasi_raqami = models.CharField(max_length=50, help_text='Ruyhatdan o\'tish guvohnomasi raqami')
    
    passport_image = models.FileField(upload_to='individual/passport', help_text="Pasportning shaxsiy ma'lumotlar bilan sahifasi", validators=[validate_file])
    inn = models.FileField(upload_to='individual/inn', help_text="Yakka tartibdagi tadbirkor sifatida ro'yxatdan o'tganlik guvohnomasi", validators=[validate_file])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Individual Info for {self.seller.user.email}"
    
class SellerEntrepreneur(models.Model): 
    seller = models.OneToOneField(Seller, 
                                  on_delete=models.CASCADE,
                                  related_name='entrepreneur_info')
    
    birth_date = models.DateField(null=True, blank=True)
    passport_series = models.CharField(max_length=10, help_text='Passport seriyasi')
    passport_number = models.CharField(max_length=10, help_text='Passport raqami')  
    jshshir = models.CharField(max_length=14, unique=True, help_text='JSHSHIR raqami')
    ruyhatdan_otish_guvohnamasi_raqami = models.CharField(max_length=50, help_text='Ruyhatdan o\'tish guvohnomasi raqami')
    
    passport_image = models.FileField(upload_to='entrepreneur/passport', help_text="Pasportning shaxsiy ma'lumotlar bilan sahifasi", validators=[validate_file])
    inn = models.FileField(upload_to='entrepreneur/inn', help_text="Yakka tartibdagi tadbirkor sifatida ro'yxatdan o'tganlik guvohnomasi", validators=[validate_file])

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Entrepreneur Info for {self.seller.user.email}"
    
class SellerCompany(models.Model):
    seller = models.OneToOneField(Seller, 
                                  on_delete=models.CASCADE, 
                                  related_name='company_info')
    
    company_name = models.CharField(max_length=255, help_text='Kompaniya nomi')
    stir = models.CharField(max_length=20, unique=True, help_text='STIR raqami')
    oked = models.CharField(max_length=10, help_text='OKED raqami')
    
    registration_certificate = models.FileField(upload_to='company/registration_certificate', help_text="MChJ (yoki boshqa yuridik shaxs)ni ro'yxatdan o'tkazish haqida xabarnoma yoki guvohnoma", validators=[validate_file])
    tashkilot_direktori_qarori = models.FileField(upload_to='company/tashkilot_direktori_qarori', validators=[validate_file])
    passport_image = models.FileField(upload_to='company/passport', help_text="Pasportning shaxsiy ma'lumotlar bilan sahifasi", validators=[validate_file])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"Company Info for {self.seller.user.email}"



class SellerBankAccount(models.Model):
    seller = models.ForeignKey(Seller, 
                               on_delete=models.CASCADE, 
                               related_name='bank_account')
    
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(
        max_length=16,
        validators=[validate_account_number],
        help_text='Hisob raqami'
        )
    
    bank_code = models.CharField(max_length=5, help_text='Bank Kodi(MFO)')   
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Bank Account for {self.seller.user.email} - {self.bank_name}"

    
class Shartnoma(models.Model):
    seller = models.ForeignKey(Seller, 
                               on_delete=models.CASCADE, 
                               related_name='shartnoma')
    
    shartnoma_raqami = models.CharField(max_length=20, unique=True, default=f"{random.randint(1000000, 9999999)}s")
    
    tasdiqlash_screenshoti_or_rasmi = models.FileField(upload_to='shartnoma/documents', validators=[validate_file], null=True, blank=True)
    signed_at = models.DateTimeField(auto_now_add=True)
    from_date = models.DateTimeField(default=timezone.now)
    to_date = models.DateTimeField(default=timezone.now() + timedelta(days=365 * 5))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
    def __str__(self):
        return f"Shartnoma for {self.seller.user.email} signed at {self.signed_at}"


class SellerBalance(models.Model):
    seller = models.OneToOneField(Seller, 
                                  on_delete=models.CASCADE, 
                                  related_name='balance')
    
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    
    available_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Balance for {self.seller.user.email}: {self.amount}"


