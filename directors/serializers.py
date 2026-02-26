from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class DirectorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'phone_number', 
            'birth_date', 'gender', 'avatar', 'address', 'role'
        ]
        read_only_fields = ['id', 'role', 'email', 'username']
