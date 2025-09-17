from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Право владельца"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsProfileOwner(BasePermission):
    """Право владельца профиля"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
