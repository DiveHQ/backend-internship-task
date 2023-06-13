from core.constants import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import UserFilter
from .models import UserSettings
from .permissions import IsAccountOwner, IsUserManager
from .serializers import PasswordSerializer, UserSerializer, UserSettingsSerializer


class UserViewSet(ModelViewSet):
    """User model view set."""

    queryset = User.objects.all()
    permission_classes = [IsUserManager | IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == "update_password":
            return PasswordSerializer
        return UserSerializer

    @action(
        detail=True,
        methods=["patch"],
        url_path="update-password",
        permission_classes=[IsAccountOwner],
    )
    def update_password(self, request: Request, pk):
        """Update only the password of a user. Allows permission only to the account owner."""
        return super().update(request, pk)


class UserSettingViewSet(
    GenericViewSet,
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
