from django.db import models
from django.conf import settings

class Queue(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('ongoing', 'Qabulda'),
        ('completed', 'Yakunlandi'),
        ('skipped', 'O‘tkazib yuborildi'),
    )

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_queues')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='patient_queues')
    number = models.PositiveIntegerField() # Navbat raqami
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Vaqtlar
    scheduled_time = models.DateTimeField() # Rejalashtirilgan vaqt
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_time', 'number']
        unique_together = ['doctor', 'scheduled_time', 'number']

    def __str__(self):
        return f"#{self.number} - {self.patient.full_name} -> {self.doctor.user.full_name}"

# --- Kutish zali (Call Center Queue) ---
class ReceptionWaitingQueue(models.Model):
    patient = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='waiting_status'
    )
    hospital = models.ForeignKey(
        'hospitals.Hospital', 
        on_delete=models.CASCADE
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['joined_at'] # Birinchi kelgan birinchi xizmat oladi

    def __str__(self):
        return f"Waiting: {self.patient.full_name}"