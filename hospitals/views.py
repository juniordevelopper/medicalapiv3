from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from admins.permissions import *

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAdminRole]
        return [permission() for permission in permission_classes]

class HospitalViewSet(viewsets.ModelViewSet):
    """
    Shifoxonalarni boshqarish uchun ViewSet.
    Faqat Admin role'ga ega foydalanuvchilar uchun.
    """
    # 'images' ni olib tashladik, chunki u endi ManyToMany yoki ForeignKey emas.
    # 'image' (singular) maydoni select_related yoki prefetch_related talab qilmaydi.
    queryset = Hospital.objects.all().select_related(
        'region', 
        'director'
    ).prefetch_related(
        'departments'
    )
    
    serializer_class = HospitalSerializer
    permission_classes = [IsAdminRole]

    def get_serializer_context(self):
        """
        Serializer ichida 'request' obyektidan foydalanishimiz (rasm URL'lari uchun)
        va u yerda xatolik chiqmasligi uchun context yuboramiz.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context