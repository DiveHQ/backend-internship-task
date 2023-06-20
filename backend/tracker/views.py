from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import EntryFilter
from .models import Entry
from .serializers import EntrySerializer


# Create your views here.
class EntryViewSet(ModelViewSet):
    """User model view set."""

    queryset = Entry.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = EntrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EntryFilter

    def get_queryset(self):
        """
        If the request user is an admin, return all entries; otherwise,
        return only the entries assigned to the request user.
        """
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        """Assign request user to the entry on creation."""
        serializer.save(user=self.request.user)
