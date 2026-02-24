from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils import timezone

class UserManager(BaseUserManager):
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


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('user', 'User'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
        
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=200, choices=ROLES, default='user')
    is_verified = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=200,blank=True)
    surname = models.CharField(max_length=200, blank=True)
    father_name = models.CharField(max_length=200, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=200, choices=[('male', 'Male'),('female', 'Female')], blank=True)
    phone = models.CharField(max_length=9, blank=True)
    
    def __str__(self):
        return self.name
    

class Taker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_takers')
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone = models.CharField(max_length=9)