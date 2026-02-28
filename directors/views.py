from rest_framework import generics, viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.db import transaction
from doctors.models import *
from receptions.models import *
from .serializers import *
from .permissions import *
from doctors.serializers import *
from receptions.serializers import *

User = get_user_model()

class DirectorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DirectorProfileSerializer
    permission_classes = [IsDirectorRole]

    def get_object(self):
        return self.request.user

class DirectorDoctorManagementViewSet(viewsets.ModelViewSet):
    serializer_class = DirectorDoctorSerializer
    permission_classes = [IsDirectorOfHospital]

    def get_queryset(self):
        # Direktor faqat o'z shifoxonasi shifokorlarini ko'radi
        return Doctor.objects.filter(hospital=self.request.user.managed_hospital)

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        dept_id = request.data.get('department')
        hospital = request.user.managed_hospital

        # 1. Faqat 'patient' rolidagi bo'sh user bo'lishi shart
        user = User.objects.filter(id=user_id, role='patient').first()
        if not user:
            return Response({"error": "Faqat bo'sh foydalanuvchini shifokor etib tayinlash mumkin!"}, status=400)

        # 2. Bo'lim ushbu shifoxonaga tegishlimi?
        if not hospital.departments.filter(id=dept_id).exists():
            return Response({"error": "Ushbu bo'lim sizning shifoxonangizda mavjud emas!"}, status=400)

        with transaction.atomic():
            # 3. Rolni o'zgartirish
            user.role = 'doctor'
            user.save()
            
            # 4. Doctor obyektini yaratish
            doctor = Doctor.objects.create(
                user=user,
                hospital=hospital,
                department_id=dept_id,
                experience_years=request.data.get('experience_years', 0),
                bio=request.data.get('bio', '')
            )

        serializer = self.get_serializer(doctor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Shifokor yaratilayotganda xona raqamini ham saqlaydi
        serializer.save(
            hospital=self.request.user.managed_hospital,
            room_number=self.request.data.get('room_number')
        )

    def perform_update(self, serializer):
        # Xona raqamini keyinchalik o'zgartirish imkoniyati
        serializer.save(room_number=self.request.data.get('room_number'))

class DirectorReceptionManagementViewSet(viewsets.ModelViewSet):
    serializer_class = DirectorReceptionSerializer
    permission_classes = [IsDirectorOfHospital]

    def get_queryset(self):
        # Director faqat o'z shifoxonasi receptionlarini boshqaradi
        return Reception.objects.filter(hospital=self.request.user.managed_hospital)

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        # 1. Userni tekshirish: faqat roli 'patient' bo'lgan bo'sh user
        user = User.objects.filter(id=user_id, role='patient').first()
        
        if not user:
            return Response(
                {"error": "Faqat bo'sh (patient) foydalanuvchini reception etib tayinlash mumkin!"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # 2. User rolini o'zgartirish
            user.role = 'reception'
            user.save()
            
            # 3. Reception obyektini yaratish
            reception = Reception.objects.create(
                user=user,
                hospital=request.user.managed_hospital,
                shift_info=request.data.get('shift_info', '')
            )
            
        serializer = self.get_serializer(reception)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user

        try:
            with transaction.atomic():
                # 1. Reception obyektini o'chirish
                instance.delete()
                
                # 2. User rolini qayta 'patient' (oddiy user) holatiga qaytarish
                user.role = 'patient'
                user.save()

            return Response(
                {"msg": f"{user.full_name} ishdan bo'shatildi va roli 'patient'ga qaytarildi."}, 
                status=status.HTTP_200_OK # 204 o'rniga 200 ishlatilsa, xabar frontga yetib boradi
            )
        except Exception as e:
            return Response(
                {"error": "Xodimni bo'shatishda xatolik yuz berdi."}, 
                status=status.HTTP_400_BAD_REQUEST
            )