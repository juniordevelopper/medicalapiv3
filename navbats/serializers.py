from rest_framework import serializers
from .models import Queue
from django.utils import timezone

class BookingSerializer(serializers.ModelSerializer):
    waiting_count = serializers.SerializerMethodField()
    estimated_waiting_time = serializers.SerializerMethodField()
    room = serializers.CharField(source='doctor.room_number', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.full_name', read_only=True)

    class Meta:
        model = Queue
        fields = ['id', 'doctor_name', 'room', 'number', 'status', 'waiting_count', 'estimated_waiting_time', 'scheduled_time']
        read_only_fields = ['number', 'status', 'scheduled_time']

    def get_waiting_count(self, obj):
        # Shifokor qabulida kutilayotgan bemorlar soni
        return Queue.objects.filter(doctor=obj.doctor, status='pending').count()

    def get_estimated_waiting_time(self, obj):
        # Har bir bemor uchun 10 daqiqadan hisob-kitob
        count = self.get_waiting_count(obj)
        return count * 10 # minutlarda
