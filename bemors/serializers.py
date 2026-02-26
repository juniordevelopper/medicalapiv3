from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'phone_number', 
            'birth_date', 'gender', 'blood_group', 'avatar', 'address'
        ]
        read_only_fields = ['id', 'email', 'username']
