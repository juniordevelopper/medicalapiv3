from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart")
        if not username:
            raise ValueError("Username kiritilishi shart")
            
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('director', 'Director'),
        ('doctor', 'Doctor'),
        ('reception', 'Reception'),
        ('patient', 'Patient'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Erkak'),
        ('female', 'Ayol'),
    )

    # --- Ro'yxatdan o'tishda majburiy maydonlar ---
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255) # Ro'yxatdan o'tganda kiritiladi
    
    # --- Profilni tahrirlashda to'ldiriladigan ixtiyoriy maydonlar ---
    phone_regex = RegexValidator(regex=r'^\+998\d{9}$', message="Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    
    # --- Tizim holati va Rollar ---
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    is_active = models.BooleanField(default=True) # Admin block qilishi uchun
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False) # Email verification uchun
    
    # --- Accountni o'chirish (3 kunlik kutish mantiqi uchun) ---
    delete_requested = models.BooleanField(default=False)
    delete_reason = models.TextField(blank=True, null=True)
    delete_requested_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    # Login jarayoni uchun sozlamalar
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.role})"
