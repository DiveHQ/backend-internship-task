from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


def check_auth(request):
    return request.user.is_authenticated


class IsOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        else:
            return obj.user == request.user


class IsActive(BasePermission):
    def has_permission(self, request, view):
        return (
            check_auth(request)
            and request.user.deleted is False
            and request.user.is_active is True
        )


class IsTask(BasePermission):
    def has_permission(self, request, view):
        if not settings.GOOGLE_CLOUD_TASKS_ON_GAE or request.META.get(
            "HTTP_X_APPENGINE_QUEUENAME"
        ):
            return True
        return False


class IsCron(BasePermission):
    def has_permission(self, request, view):
        if request.headers.get("X-Appengine-Cron"):
            return True
        return False
