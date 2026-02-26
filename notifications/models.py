from django.db import models
from django.conf import settings

class DeletionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlandi (O‘chirildi)'),
        ('rejected', 'Rad etildi'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deletion_requests')
    reason = models.TextField(verbose_name="O'chirish sababi")
    admin_feedback = models.TextField(null=True, blank=True, verbose_name="Admin javobi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
