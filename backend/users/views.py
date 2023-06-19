from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from backend.utils.createResponse import createResponse

from .models import User
from .permissions import IsSameUser
from .serializers import UserSerializer


class UserProfile(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, or modify a user's profile.
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSameUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_204_NO_CONTENT,
        ):
            if request.method in ("PUT", "PATCH"):
                message = "User updated successfully"
            elif request.method == "DELETE":
                message = "User deleted successfully"
            else:
                message = "User retreived successfully"
            response = createResponse(
                message=message,
                success=True,
                data=response.data,
                status_code=response.status_code,
            )
        return super().finalize_response(request, response, *args, **kwargs)


class Register(CreateAPIView):
    """
    Register a user.
    """

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_201_CREATED:
            response = createResponse(
                message="User registered successfully",
                success=True,
                data=response.data,
                status_code=response.status_code,
            )
        return super().finalize_response(request, response, *args, **kwargs)


class Login(TokenObtainPairView):
    """
    Login a user.
    """

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            response = createResponse(
                message="User logged in successfully",
                success=True,
                data=response.data,
                status_code=response.status_code,
            )
        return super().finalize_response(request, response, *args, **kwargs)


class RefreshToken(TokenRefreshView):
    """
    Refresh a user's token.
    """

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK:
            response = createResponse(
                message="Token refreshed successfully",
                success=True,
                data=response.data,
                status_code=response.status_code,
            )
        return super().finalize_response(request, response, *args, **kwargs)
