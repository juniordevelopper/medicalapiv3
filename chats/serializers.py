from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'sender_role', 'text', 'file', 'is_read', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    patient_avatar = serializers.ImageField(source='patient.avatar', read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'patient_name', 'patient_avatar', 'is_active', 'last_message', 'created_at']

    def get_last_message(self, obj):
        msg = obj.messages.last()
        return msg.text if msg else "Fayl yuborildi" if msg and msg.file else None
