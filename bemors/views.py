from rest_framework import generics, viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import *
from doctors.serializers import *
from hospitals.serializers import *
from hospitals.models import *
from doctors.models import *
from notifications.serializers import *
from notifications.models import *

User = get_user_model()

class PatientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class PatientHospitalListView(generics.ListAPIView):
    # Hudud bo'yicha filterlash keyinroq django-filter bilan qo'shiladi
    queryset = Hospital.objects.all()
    serializer_class = ... # HospitalSerializer avvalroq yozilgan

class HospitalListView(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    filterset_fields = ['region'] # ?region=1 deb filterlash uchun

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorProfileSerializer
    filterset_fields = ['hospital', 'department'] # ?hospital=1&department=2


class PatientDeleteRequestView(generics.CreateAPIView):
    serializer_class = DeletionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # So'rovni yaratish va User modelida bayroqni yoqish
        serializer.save(user=self.request.user)
        self.request.user.delete_requested = True
        self.request.user.save()