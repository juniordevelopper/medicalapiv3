from django.db import models
from django.conf import settings
from django.db import transaction

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE, related_name='doctors')
    department = models.ForeignKey('hospitals.Department', on_delete=models.PROTECT, related_name='doctors_list')
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    room_number = models.CharField(max_length=10, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        # Ishdan bo'shatilganda foydalanuvchi rolini yana 'patient'ga qaytarish
        with transaction.atomic():
            user = self.user
            user.role = 'patient'
            user.save()
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.department.name}"
