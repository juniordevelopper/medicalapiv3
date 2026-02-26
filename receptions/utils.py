from .models import Reception, ReceptionWaitingQueue
from django.conf import settings
import os

def get_available_operator(hospital_id):
    """Smenada va bo'sh bo'lgan birinchi operatorni qaytaradi"""
    return Reception.objects.filter(
        hospital_id=hospital_id, 
        is_online=True, 
        is_available=True
    ).first()

def get_waiting_audio_url():
    """Bemorlar uchun umumiy ovozli xabar yo'li"""
    # Media papkangizda 'audio/waiting_announcement.mp3' bo'lishi kerak
    return os.path.join(settings.MEDIA_URL, 'audio/waiting_announcement.mp3')
