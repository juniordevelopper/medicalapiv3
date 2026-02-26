from django.db import models
from django.conf import settings

class Reception(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reception_profile'
    )
    hospital = models.ForeignKey(
        'hospitals.Hospital', 
        on_delete=models.CASCADE, 
        related_name='receptions'
    )
    # --- Yangi maydonlar ---
    is_available = models.BooleanField(default=False, verbose_name="Bo'sh / Band")
    is_online = models.BooleanField(default=False, verbose_name="Smenada / Smenada emas")
    current_patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='current_call'
    )
    
    shift_info = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.hospital.name})"
