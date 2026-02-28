from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class DoctorChatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Shifokor faqat o'zining faol chatlarini ko'radi
        return Conversation.objects.filter(doctor__user=self.request.user, is_active=True).order_by('-created_at')

    # Xabarlar tarixini olish: GET /api/v1/doctor/conversations/{id}/messages/
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        msgs = conversation.messages.all().order_by('created_at')
        serializer = MessageSerializer(msgs, many=True)
        return Response(serializer.data)

    # Fayl/Audio yuborish: POST /api/v1/doctor/conversations/{id}/send_message/
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation=conversation, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)