from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            id = urlsafe_base64_decode(attrs['uidb64']).decode()
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
                raise serializers.ValidationError('Token yaroqsiz yoki muddati o‘tgan.')
        except Exception:
            raise serializers.ValidationError('Xatolik yuz berdi.')
        return attrs
