from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'file', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['id', 'doctor', 'patient', 'is_active', 'messages', 'created_at']
