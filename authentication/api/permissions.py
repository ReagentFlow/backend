from rest_framework.permissions import BasePermission, SAFE_METHODS
from authentication.models import User


class IsAuthenticatedAndAdmin(BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return bool(request.user and request.user.is_authenticated and role == User.ADMIN)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            role == User.ADMIN
        )
