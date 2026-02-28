from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from locations.models import *

class Department(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Bo'lim nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Bo'lim haqida ma'lumot")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"
        ordering = ['name']


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey('locations.Region', on_delete=models.PROTECT, related_name='hospitals')
    departments = models.ManyToManyField('hospitals.Department', related_name='hospitals')
    address = models.TextField()
    image = models.ImageField(upload_to='hospitals/photos/', null=True, blank=True)
    
    director = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_hospital'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.director:
            # 1. Admin o'zini direktor qila olmaydi
            if self.director.role == 'admin':
                raise ValidationError("Adminni shifoxona direktori etib tayinlab bo'lmaydi!")
            
            # 2. Allaqachon boshqa shifoxonada band bo'lganlarni tekshirish
            # (Agar foydalanuvchi role 'patient' bo'lmasa, demak u allaqachon band: director, doctor yoki reception)
            if self.director.role != 'patient' and self.director.role != 'director':
                raise ValidationError(f"Bu foydalanuvchi allaqachon tizimda {self.director.role} vazifasida ishlaydi!")

            # 3. Agar u allaqachon boshqa shifoxona direktori bo'lsa
            existing = Hospital.objects.filter(director=self.director).exclude(id=self.id)
            if existing.exists():
                raise ValidationError("Bu foydalanuvchi allaqachon boshqa shifoxona direktori!")

    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Tranzaksiya orqali ham shifoxonani saqlaymiz, ham user rolini o'zgartiramiz
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.director and self.director.role == 'patient':
                self.director.role = 'director'
                self.director.save()

    def __str__(self):
        return self.name