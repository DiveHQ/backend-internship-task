from rest_framework.viewsets import ModelViewSet

from api_project.common.permissions import IsAdmin, IsOwner

from .models import Calories
from .serializers import CaloriesSerializer


class CaloriesView(ModelViewSet):
    queryset = Calories.objects.all()
    serializer_class = CaloriesSerializer
    permission_classes = [IsOwner | IsAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == user.Roles.ADMIN:
            serializer.save()
        serializer.save(user=user)
