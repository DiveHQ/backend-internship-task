from django.http import HttpRequest
from rest_framework.permissions import BasePermission, IsAuthenticated

from .constants import USER_MANAGER_GROUP, User


class IsUserManager(BasePermission):
    """Allows access only to user managers."""

    def has_permission(self, request: HttpRequest, view):
        return request.user.groups.filter(name=USER_MANAGER_GROUP).exists()


class IsAccountOwner(IsAuthenticated):
    """Allows access to users who own the account/user object."""

    def has_object_permission(self, request: HttpRequest, view, obj: User):
        return request.user == obj
