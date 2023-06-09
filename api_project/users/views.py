from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import SignupResponseSerializer, SignUpSerializer, UserSerializer

User = get_user_model()


class UserView(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """
    User viewset
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @swagger_auto_schema(method="GET", responses={200: UserSerializer})
    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="User signup", responses={201: SignupResponseSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = SignupResponseSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
