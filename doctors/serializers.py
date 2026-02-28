from rest_framework import serializers
from .models import Doctor
from django.contrib.auth import get_user_model

User = get_user_model()

class DirectorDoctorSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'user_details', 'department', 'department_name', 'experience_years', 'bio', 'room_number']

    def get_user_details(self, obj):
        return {
            "full_name": obj.user.full_name,
            "phone": obj.user.phone_number,
            "email": obj.user.email
        }

class DoctorProfileSerializer(serializers.ModelSerializer):
    # Foydalanuvchi ma'lumotlari (ism, tel va h.k.)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'full_name', 'email', 'hospital_name', 
            'department_name', 'experience_years', 'bio'
        ]
        read_only_fields = ['id', 'hospital_name', 'department_name']