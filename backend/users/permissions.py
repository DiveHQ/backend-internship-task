from rest_framework import permissions


# Allow the user to modify himself only
class IsSameUser(permissions.BasePermission):
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
