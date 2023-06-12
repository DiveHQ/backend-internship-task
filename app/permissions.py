from rest_framework.permissions import BasePermission, SAFE_METHODS



class UserEditDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.email == request.user.email
    
class ManagerEditDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Manager'
    
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

