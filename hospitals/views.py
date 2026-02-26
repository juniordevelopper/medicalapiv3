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
    queryset = Hospital.objects.all().select_related('region', 'director').prefetch_related('departments', 'images')
    serializer_class = HospitalSerializer
    permission_classes = [IsAdminRole]

    def create(self, request, *args, **kwargs):
        # Rasmlar bilan birga yaratish (Form-data orqali)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hospital = serializer.save()
        
        # Rasmlarni saqlash
        images = request.FILES.getlist('images')
        for image in images:
            HospitalImage.objects.create(hospital=hospital, image=image)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)