from rest_framework import permissions


class IsAdminOrUserManager(permissions.BasePermission):
    """
    Custom permission to only allow admins and user managers.
    """

    def has_permission(self, request, view):
        if request.user.is_admin or request.user.is_user_manager:
            return True