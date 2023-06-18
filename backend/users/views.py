from rest_framework import permissions, status
from rest_framework.views import APIView

from backend.utils.createResponse import createResponse


# Create your views here.
class RootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return createResponse(
            message="Welcome to the backend!",
            status_code=status.HTTP_200_OK,
            success=True,
        )
