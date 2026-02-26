from rest_framework import permissions

class IsDirectorRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'director'
        )


class IsDirectorOfHospital(permissions.BasePermission):
    """
    Faqat direktor o'z shifoxonasiga xodim biriktira olishi uchun.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'director' and
            hasattr(request.user, 'managed_hospital') # Shifoxonasi bormi?
        )

    def has_object_permission(self, request, view, obj):
        # Agar ob'ekt (doctor/reception) direktorning shifoxonasiga tegishli bo'lsa
        return obj.hospital == request.user.managed_hospital