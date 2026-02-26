from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class HospitalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalImage
        fields = ['id', 'image']

class HospitalSerializer(serializers.ModelSerializer):
    images = HospitalImageSerializer(many=True, read_only=True)
    # Frontend uchun faqat 'patient' rolidagi (ya'ni hali xodim bo'lmagan) userlarni chiqarish
    director_candidates = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = [
            'id', 'name', 'region', 'departments', 
            'address', 'director', 'images', 'director_candidates',
            'created_at', 'updated_at'
        ]

    def get_director_candidates(self, obj):
        from accounts.models import User
        # Faqat roli 'patient' bo'lgan va hali hech qanday shifoxonaga biriktirilmagan userlar
        return User.objects.filter(
            role='patient', 
            is_active=True
        ).values('id', 'full_name', 'email', 'username')

    def create(self, validated_data):
        # Ko'p rasm yuklash mantiqi (agar kerak bo'lsa)
        return super().create(validated_data)