from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .serializers import *
from admins.serializers import *
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 1. Token va UID yaratish
        token = PasswordResetTokenGenerator().make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        
        # 2. Dinamik IP manzilni aniqlash
        # Port 3000 (React) uchun link yaratish
        current_host = request.get_host().split(':')[0]
        link = f"http://{current_host}:5173/auth/verify-email/{uidb64}/{token}/"
        
        # 3. Chiroyli HTML shablon
        subject = "Medical Online - Email manzilini tasdiqlash"
        html_content = f"""
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; color: #1e293b; max-width: 600px; margin: auto; border: 1px solid #e2e8f0; border-radius: 16px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h1 style="color: #2563eb; margin: 0;">Medical Online</h1>
                </div>
                <h2 style="font-size: 1.5rem; color: #0f172a;">Xush kelibsiz, {user.full_name}!</h2>
                <p style="font-size: 1rem; line-height: 1.6; color: #475569;">
                    Ro'yxatdan o'tganingizdan xursandmiz. Tizimning barcha imkoniyatlaridan foydalanish uchun, iltimos, email manzilingizni tasdiqlang.
                </p>
                <div style="text-align: center; margin: 35px 0;">
                    <a href="{link}" style="background-color: #2563eb; color: white; padding: 14px 30px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 1rem; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);">
                        Emailni tasdiqlash
                    </a>
                </div>
                <p style="font-size: 0.9rem; color: #64748b;">
                    Agar tugma ishlamasa, ushbu havolani brauzerga nusxalab joylang:<br>
                    <a href="{link}" style="color: #2563eb; word-break: break-all;">{link}</a>
                </p>
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;">
                <p style="font-size: 0.8rem; color: #94a3b8; text-align: center;">
                    Bu xabar avtomatik yuborildi. Iltimos, unga javob bermang. <br>
                    &copy; 2026 Medical Online jamoasi.
                </p>
            </div>
        """
        
        # 4. Emailni yuborish (HTML va Text versiyalari bilan)
        text_content = strip_tags(html_content) # HTMLni tushunmaydigan mijozlar uchun matn
        msg = EmailMultiAlternatives(
            subject, 
            text_content, 
            "Medical Online <noreply@medicalonline.uz>", 
            [user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return Response({
            "msg": "Muvaffaqiyatli ro'yxatdan o'tdingiz. Emailingizni tasdiqlash uchun xat yuborildi.",
            "email": user.email
        }, status=status.HTTP_201_CREATED)

class VerifyEmailView(views.APIView):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if PasswordResetTokenGenerator().check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({"msg": "Email tasdiqlandi!"}, status=status.HTTP_200_OK)
            return Response({"error": "Token yaroqsiz"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Xatolik"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            
            # IP dinamik bo'lgani uchun request'dan hostni olamiz
            current_site = request.get_host() 
            link = f"http://{current_site.split(':')[0]}:5173/auth/password-confirm/{uidb64}/{token}/"
            
            subject = "Medical Online - Parolni tiklash so'rovi"
            html_content = f"""
                <div style="font-family: sans-serif; padding: 20px; border: 1px solid #eee; border-radius: 10px; max-width: 500px;">
                    <div style="text-align: center; margin-bottom: 20px;">
                        <h1 style="color: #2563eb; margin: 0;">Medical Online</h1>
                    </div>
                    <h2 style="color: #2563eb;">Salom, {user.full_name}!</h2>
                    <p>Biz sizning hisobingizdan parolni tiklash bo'yicha so'rov oldik.</p>
                    <p>Agar bu siz bo'lsangiz, parolni o'zgartirish uchun quyidagi tugmani bosing:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{link}" style="background-color: #2563eb; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-weight: bold;">Parolni o'zgartirish</a>
                    </div>
                    <p style="color: #64748b; font-size: 0.9rem;">Agar siz bu so'rovni yubormagan bo'lsangiz, shunchaki ushbu xatga e'tibor bermang yoki qo'llab-quvvatlash xizmati bilan bog'laning.</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="font-size: 0.8rem; color: #94a3b8;">Medical Online jamoasi</p>
                </div>
            """
            
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(
                subject, 
                text_content, 
                "Medical Online <noreply@medicalonline.uz>", 
                [user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response(
                {"msg": "Parolni tiklash havolasi emailga yuborildi"}, 
                status=status.HTTP_200_OK
            )

        return Response(
            {"msg": "Agar ushbu email tizimda mavjud bo'lsa, xat yuborildi"}, 
            status=status.HTTP_200_OK
        )

class PasswordResetConfirmView(views.APIView):
    def patch(self, request, *args, **kwargs):
        password = request.data.get('password')
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')

        try:
            # IDni dekod qilish
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            # Tokenni tekshirish
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token yaroqsiz yoki muddati o'tgan"}, status=status.HTTP_400_BAD_REQUEST)

            # Parolni yangilash
            user.set_password(password)
            user.save()
            return Response({"msg": "Parol muvaffaqiyatli yangilandi"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Xatolik yuz berdi"}, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(generics.RetrieveAPIView):
    """
    Token orqali joriy foydalanuvchini aniqlaydi 
    va uning ma'lumotlarini qaytaradi.
    """
    serializer_class = UserMeSerializer
    permission_classes = [permissions.IsAuthenticated] # Faqat login qilganlar uchun

    def get_object(self):
        # request.user - bu tokendan aniqlangan joriy foydalanuvchi
        return self.request.user