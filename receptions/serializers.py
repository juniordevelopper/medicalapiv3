from rest_framework import serializers
from .models import Reception
from django.contrib.auth import get_user_model

User = get_user_model()

class ReceptionProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta:
        model = Reception
        fields = ['id', 'full_name', 'hospital_name', 'shift_info']
        read_only_fields = ['id', 'hospital_name']

class DirectorReceptionSerializer(serializers.ModelSerializer):
    # Foydalanuvchi ma'lumotlarini ko'rish uchun
    user_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Reception
        fields = ['id', 'user', 'user_details', 'shift_info', 'created_at', 'updated_at']

    def get_user_details(self, obj):
        return {
            "full_name": obj.user.full_name,
            "email": obj.user.email,
            "phone": obj.user.phone_number
        }

