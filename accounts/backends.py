from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Username maydoni orqali ham emailni, ham usernameni tekshiramiz
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
