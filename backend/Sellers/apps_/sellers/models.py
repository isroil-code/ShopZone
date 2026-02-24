from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .validators import validate_file, validate_account_number
import random
from datetime import timedelta

class SellerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email majburiy")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True bo'lishi shart")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True bo'lishi shart")

        return self.create_user(email, password, **extra_fields)



class Seller(AbstractBaseUser, PermissionsMixin):
    
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
    
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    
    biznes_type = models.CharField(max_length=50, choices=BusinessType.choices, null=True, blank=True)
    phone = models.CharField(max_length=9, unique=True, help_text='Telefon raqami (9 ta raqam)')

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_verified = models.BooleanField(default=False)    
    
    
    objects = SellerManager()
    
    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers' 
        indexes = [
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.email} - Seller"
    
    
    

class SellerPersonalInformation(models.Model):
    seller = models.OneToOneField(Seller, 
                                  on_delete=models.CASCADE, 
                                  related_name='profile')
    
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number2 = models.CharField(max_length=20, help_text='qushimcha telefon raqam')
    father_name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Information for {self.seller.email} {self.name}"
    
    
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
        return f"Individual Info for {self.seller.email}"
    
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
        return f"Entrepreneur Info for {self.seller.email}"
    
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
        return f"Company Info for {self.seller.email}"



class SellerBankAccount(models.Model):
    seller = models.ForeignKey(Seller, 
                               on_delete=models.CASCADE, 
                               related_name='bank_account')
    
    bank_name = models.CharField(max_length=255)
    holder_name = models.CharField(max_length=255, help_text='Hisob egasining ismi')
    account_number = models.CharField(
        max_length=16,
        validators=[validate_account_number],
        help_text='Hisob raqami'
        )
    
    bank_code = models.CharField(max_length=5, help_text='Bank Kodi(MFO)')   
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Bank Account for {self.seller.email} - {self.bank_name}"

    
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
        return f"Shartnoma for {self.seller.email} signed at {self.signed_at}"


class SellerBalance(models.Model):
    seller = models.OneToOneField(Seller, 
                                  on_delete=models.CASCADE, 
                                  related_name='balance')
    
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Balance for {self.seller.email}: {self.amount}"


class SellerMoneyTransfer(models.Model):
    seller = models.ForeignKey(Seller, 
                               on_delete=models.CASCADE, 
                               related_name='seller_transfers')
    
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    reference_id = models.CharField(max_length=100)
    
    which_account = models.CharField(max_length=100)
    transfer_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.seller.email}: {self.amount} on {self.transfer_date}"
    
    
