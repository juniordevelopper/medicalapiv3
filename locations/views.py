from rest_framework import viewsets, permissions
from .models import Region
from .serializers import RegionSerializer
from admins.permissions import IsAdminRole

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny] # Hamma ko'ra oladi
        else:
            permission_classes = [IsAdminRole] # Faqat admin o'zgartira oladi
        return [permission() for permission in permission_classes]
