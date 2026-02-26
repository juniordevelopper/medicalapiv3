from rest_framework import permissions

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        # request.user.role ni kichik harflarda ekanligini tekshiring
        return bool(
            request.user and 
            request.user.is_authenticated and 
            str(request.user.role).lower() == 'admin'
        )
