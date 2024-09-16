from rest_framework.permissions import SAFE_METHODS, BasePermission

from authentication.models import User


class IsAuthenticatedAndAdmin(BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return bool(request.user and request.user.is_authenticated and role == User.ADMIN)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        is_auth = request.user and request.user.is_authenticated
        return bool(request.method in SAFE_METHODS and is_auth or is_auth and request.user.role == User.ADMIN)
