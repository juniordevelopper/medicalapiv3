from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class HospitalSerializer(serializers.ModelSerializer):
    director_candidates = serializers.SerializerMethodField()
    region_details = serializers.SerializerMethodField()
    department_details = serializers.SerializerMethodField()
    director_name = serializers.CharField(source='director.full_name', read_only=True)

    class Meta:
        model = Hospital
        fields = [
            'id', 'name', 'region', 'departments', 'region_details',
            'address', 'director', 'image', 'director_candidates', 
            'director_name', 'department_details', 'created_at', 'updated_at'
        ]

    def get_director_candidates(self, obj):
        from accounts.models import User
        return User.objects.filter(role='patient', is_active=True).values('id', 'full_name', 'email', 'username')

    def get_region_details(self, obj):
        return {"id": obj.region.id, "name": obj.region.name} if obj.region else None

    def get_department_details(self, obj):
        return [{"id": d.id, "name": d.name} for d in obj.departments.all()]

    def update(self, instance, validated_data):
        # Direktor mantiqi (agar bo'sh kelsa None qilish)
        if 'director' in validated_data and validated_data['director'] == "":
            validated_data['director'] = None
        
        # Bo'limlarni yangilash
        depts = validated_data.pop('departments', None)
        if depts is not None:
            instance.departments.set(depts)

        return super().update(instance, validated_data)