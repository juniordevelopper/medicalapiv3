from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from navbats.models import Queue
from django.core.mail import send_mail
from django.utils import timezone
from .permissions import *
from .models import *
from .serializers import *
from chats.models import *

class DoctorSelfProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsDoctorRole]

    def get_object(self):
        # Tizimga kirgan userga tegishli doctor obyektini qaytaradi
        return Doctor.objects.get(user=self.request.user)

class DoctorQueueViewSet(viewsets.ViewSet):
    permission_classes = [IsDoctorRole]

    @action(detail=True, methods=['post'])
    def skip_patient(self, request, pk=None):
        queue = Queue.objects.get(pk=pk, doctor__user=request.user)
        queue.status = 'skipped'
        queue.save()

        # Email yuborish mantiqi
        subject = "Navbatni o'tkazib yubordingiz"
        message = (
            f"Hurmatli {queue.patient.full_name}!\n\n"
            f"Siz {queue.doctor.hospital.name} shifoxonasi, "
            f"{queue.doctor.department.name} bo'limidagi "
            f"Dr. {queue.doctor.user.full_name} qabuliga belgilangan "
            f"#{queue.number}-raqamli navbatingizni o'tkazib yubordingiz.\n"
            f"Vaqti: {queue.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [queue.patient.email])

        return Response({"msg": "Bemor o'tkazib yuborildi va email xabarnoma ketdi."})

    @action(detail=False, methods=['get'])
    def my_patients_history(self, request):
        # Shifokor o'zi ko'rgan bemorlar tarixi
        completed_queues = Queue.objects.filter(doctor__user=request.user, status='completed')
        # Bu yerda serializer orqali bemor ma'lumotlarini (tel, email) qaytaramiz
        return Response({"history": "Bemorlar ro'yxati shu yerda chiqadi"})

    @action(detail=True, methods=['post'])
    def start_chat(self, request, pk=None):
        queue = self.get_object() # Navbatni olamiz
        
        # Chat yaratish yoki borini olish
        conversation, created = Conversation.objects.get_or_create(
            doctor=queue.doctor,
            patient=queue.patient,
            is_active=True
        )
        
        return Response({
            "msg": "Chat faollashtirildi",
            "conversation_id": conversation.id
        })
