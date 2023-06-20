from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from backend.utils.createResponse import createResponse

from .models import User, UserSettings
from .permissions import IsSameUser, IsUserManager
from .serializers import UserSerializer, UserSettingsSerializer


class UserProfile(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, or modify a user's profile.
    """

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


class ElevatedUserView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, or modify a user's profile.
    Only for managers and admins.
    """

    permission_classes = [IsUserManager | IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]


class UserSettingView(
    GenericAPIView,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    """Viewset for creating, retrieving and updating user settings."""

    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Allow access to only the settings of the request user."""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
