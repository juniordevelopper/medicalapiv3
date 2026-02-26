from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import viewsets, status, generics, filters
from navbats.models import Queue
from navbats.serializers import *
from django.utils import timezone
from .models import *
from .serializers import *
from doctors.serializers import *
from .permissions import *
from .models import *
from accounts.serializers import *

User = get_user_model()

class ReceptionSelfProfileView(viewsets.ModelViewSet):
    serializer_class = ReceptionProfileSerializer
    permission_classes = [IsReceptionRole]

    def get_queryset(self):
        return Reception.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle_status(self, request):
        """ Smenani boshlash yoki tugatish """
        reception = Reception.objects.get(user=request.user)
        reception.is_online = not reception.is_online
        reception.is_available = reception.is_online # Smenaga kirsa bo'sh bo'ladi
        reception.save()
        status_text = "Smenada" if reception.is_online else "Smenadan chiqdi"
        return Response({"status": status_text, "is_online": reception.is_online})

    @action(detail=False, methods=['post'])
    def set_busy(self, request):
        """ Qo'ng'iroq paytida band qilish """
        reception = Reception.objects.get(user=request.user)
        reception.is_available = False
        reception.save()
        return Response({"msg": "Band holatiga o'tkazildi"})

class ReceptionBookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsReceptionRole]

    def get_queryset(self):
        # Reception faqat o'z shifoxonasidagi navbatlarni ko'radi
        return Queue.objects.filter(doctor__hospital=self.request.user.reception_profile.hospital)

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient')
        doctor_id = request.data.get('doctor')
        
        # 1. Shifokorni tekshirish
        doctor = Doctor.objects.filter(id=doctor_id).first()
        if not doctor:
            return Response({"error": "Shifokor topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Bugun uchun yangi navbat raqamini olish
        last_queue = Queue.objects.filter(
            doctor=doctor, 
            created_at__date=timezone.now().date()
        ).order_by('number').last()
        
        next_number = (last_queue.number + 1) if last_queue else 1

        # 3. Navbatni yaratish
        queue = Queue.objects.create(
            patient_id=patient_id,
            doctor=doctor,
            number=next_number,
            status='pending',
            scheduled_time=timezone.now()
        )

        serializer = self.get_serializer(queue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReceptionDoctorListView(generics.ListAPIView):
    permission_classes = [IsReceptionRole]
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        # Faqat o'zi ishlaydigan shifoxonadagi doctorlar
        hospital = self.request.user.reception_profile.hospital
        return Doctor.objects.filter(hospital=hospital)

class ReceptionPatientSearchView(generics.ListAPIView):
    """
    Reception bemorni navbatga qo'yish uchun tizimdan qidirib topishi.
    Faqat 'patient' rolidagi va bloklanmagan foydalanuvchilar chiqadi.
    """
    permission_classes = [IsReceptionRole]
    serializer_class = RegisterSerializer
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'phone_number', 'username', 'email']

    def get_queryset(self):
        return User.objects.filter(role='patient', is_active=True).order_by('full_name')