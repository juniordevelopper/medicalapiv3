from django.db import models
from django.conf import settings

class Conversation(models.Model):
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True) # Shifokor chatni yopishi mumkin
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True) # Fayl, rasm, video/ovozli xabar
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
