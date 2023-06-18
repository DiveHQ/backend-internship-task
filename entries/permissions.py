from rest_framework import permissions
from .models import Entry
from django.http import Http404
from rest_framework.exceptions import ValidationError


class EntriesCreateObjectLevelPermission(permissions.BasePermission):
    """
    Object-level permission to allow admin access to all objects and user access to their own objects.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to create an entry.

        The user must provide a valid user_id in the request data.
        Admins have access to all objects, while regular users can only access their own objects.

        Returns True if the user has permission, False otherwise.
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return False

        if request.user.is_admin or int(user_id) == int(request.user.id):
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the specified entry object.

        Admins have access to all objects, while regular users can only access their own objects.

        Returns True if the user has permission, False otherwise.
        """
        if request.user.is_admin or str(obj.user.id) == str(request.user.id):
            return True

        return False

    def has_permission_denied(self, request, message=None):
        """
        Raise a permission denied exception with an optional custom message.

        This method is called when permission is denied.

        Raises:
            permissions.PermissionDenied: Exception with a custom detail message.
        """
        if message is None:
            message = 'User ID not provided'
        raise permissions.PermissionDenied(detail=message)


class EntriesObjectLevelPermission(permissions.BasePermission):
    """
    Object-level permission to allow admin access to all objects and user access to their own objects.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action on entries.

        The user must provide a valid entry_id in the request data.
        Admins have access to all objects, while regular users can only access their own objects.

        Returns True if the user has permission, False otherwise.
        """
        entry_id = request.data.get('entry_id')
        if not entry_id:
            raise ValidationError('Entry ID not provided')
        if request.user.is_admin:
            return True
        try:
            entry = Entry.objects.get(id=entry_id)
            if str(entry.user.id) == str(request.user.id):
                return True
        except Entry.DoesNotExist:
            raise Http404("Entry does not exist")
        return False

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the specified entry object.

        Admins have access to all objects, while regular users can only access their own objects.

        Returns True if the user has permission, False otherwise.
        """
        if request.user.is_admin or str(obj.user) == str(request.user):
            return True

        return False


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins.
    """

    def has_permission(self, request, view):
        """
        Check if the user is an admin.

        Returns True if the user is an admin, False otherwise.
        """
        if request.user.is_admin:
            return True

        return False

    def has_permission_denied(self, request, message=None):
        """
        Raise a permission denied exception with an optional custom message.

        This method is called when permission is denied.

        Raises:
            permissions.PermissionDenied: Exception with a custom detail message.
        """
        if message is None:
            message = 'User is not an admin'
        raise permissions.PermissionDenied(detail=message)
