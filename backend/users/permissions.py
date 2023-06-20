from django.http import HttpRequest
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from backend.constants import USER_MANAGER_GROUP


# Allow the user to modify himself only
class IsSameUser(BasePermission):
    """
    Custom permission to only allow a user to modify herself.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj == request.user


class IsUserManager(BasePermission):
    """Allows access only to user managers."""

    def has_permission(self, request: HttpRequest, view):
        return request.user.groups.filter(name=USER_MANAGER_GROUP).exists()
