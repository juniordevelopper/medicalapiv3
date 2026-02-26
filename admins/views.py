from django.core.mail import send_mail
from rest_framework import generics, permissions
from .serializers import *
from accounts.serializers import *
from .permissions import *
from notifications.models import *
from notifications.serializers import *

class AdminProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAdminRole]

    def get_object(self):
        # Bu metod aynan so'rov yuborgan (request.user) foydalanuvchini qaytaradi
        return self.request.user


class CandidateUserListView(generics.ListAPIView):
    """Admin va Directorlar xodim tanlashi uchun bo'sh userlar ro'yxati"""
    permission_classes = [IsAdminRole]
    serializer_class = RegisterSerializer

    def get_queryset(self):
        return User.objects.filter(role='patient', is_active=True)

class AdminHandleDeleteRequestView(generics.UpdateAPIView):
    queryset = DeletionRequest.objects.all()
    serializer_class = DeletionRequestSerializer
    permission_classes = [IsAdminRole]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get('action') # 'approve' yoki 'reject'
        feedback = request.data.get('admin_feedback')

        if action == 'approve':
            # 1. Email yuborish
            send_mail(
                "Hisobingiz o'chirildi",
                f"Sizning so'rovingiz tasdiqlandi. Sabab: {feedback}",
                "admin@hospital.uz",
                [instance.user.email]
            )
            # 2. Foydalanuvchini o'chirish (DeletionRequest CASCADE tufayli o'zi ham o'chadi)
            instance.user.delete()
            return Response({"msg": "Foydalanuvchi butunlay o'chirildi"}, status=204)

        elif action == 'reject':
            # 1. Statusni yangilash
            instance.status = 'rejected'
            instance.admin_feedback = feedback
            instance.save()
            
            # 2. User modelida bayroqni o'chirish (yana so'rov yubora olishi uchun)
            instance.user.delete_requested = False
            instance.user.save()

            # 3. Profilga bildirishnoma yuborish
            Notification.objects.create(
                user=instance.user,
                title="Hisobni o'chirish rad etildi",
                message=f"Admin javobi: {feedback}"
            )
            
            # 4. Email yuborish
            send_mail("O'chirish so'rovi rad etildi", feedback, "admin@hospital.uz", [instance.user.email])
            
            return Response({"msg": "So'rov rad etildi va foydalanuvchiga xabar yuborildi"})