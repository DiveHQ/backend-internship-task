from core.constants import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import UserFilter
from .permissions import IsAccountOwner, IsUserManager
from .serializers import PasswordSerializer, UserSerializer


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
    def update_password(self, request, pk):
        """Update only the password of a user."""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
