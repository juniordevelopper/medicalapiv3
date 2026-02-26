from rest_framework import serializers
from .models import DeletionRequest, Notification

class DeletionRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = DeletionRequest
        fields = ['id', 'user', 'username', 'full_name', 'reason', 'admin_feedback', 'status', 'created_at']
        read_only_fields = ['user', 'status', 'admin_feedback']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
