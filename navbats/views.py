from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Queue
from .serializers import BookingSerializer

class PatientBookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Queue.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        doctor = serializer.validated_data['doctor']
        # Bugun uchun oxirgi navbat raqamini olish
        last_queue = Queue.objects.filter(doctor=doctor, created_at__date=timezone.now().date()).order_by('number').last()
        next_number = (last_queue.number + 1) if last_queue else 1
        
        serializer.save(
            patient=self.request.user,
            number=next_number,
            scheduled_time=timezone.now() # Real vaqtda hozirgi vaqt
        )
