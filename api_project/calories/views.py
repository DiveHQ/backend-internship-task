from rest_framework.viewsets import ModelViewSet

from api_project.common.permissions import IsAdmin, IsOwner

from .models import Calories
from .serializers import CaloriesSerializer


class CaloriesView(ModelViewSet):
    queryset = Calories.objects.all()
    serializer_class = CaloriesSerializer
    permission_classes = [IsOwner | IsAdmin]
    filterset_fields = ["user","extra" ,"calories"]
    search_fields = ["user__name", "user__email", "meal", "note"]

    def get_queryset(self):
        user = self.request.user
        if user.role == user.Roles.ADMIN:
            return self.queryset
        return self.queryset.filter(user=user)


    def perform_create(self, serializer):
        user = self.request.user
        if user.role == user.Roles.ADMIN:
            serializer.save()
        serializer.save(user=user)
