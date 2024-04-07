from rest_framework import permissions

class IsTFOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_anonymous:
                is_tf=False
            else:
                is_tf=request.user.is_tf
            return is_tf