from django.contrib.auth import get_user_model
from django.utils.timezone import now
from djoser import views as djoser_views
from djoser.compat import get_user_email
from djoser.conf import settings as djoser_settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer
from .utils import send_password_reset

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    """
    This is an example user viewset to start with in case there's too many modifications
    needed that the `CustomDjoserViewSet` doesn't provide.
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


class CustomDjoserViewSet(djoser_views.UserViewSet):
    # Delete User
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if not instance or not instance.is_active:
    #         raise NotFound("User not Found")

    #     user = request.user
    #     acc_type = user.AccountType

    #     if instance == user or user.account_type in [acc_type.ADMIN, acc_type.EMPLOYEE]:
    #         # Delete Token
    #         token = Token.objects.filter(user=instance)
    #         if token:
    #             token.first().delete()

    #         yr = now().strftime("%y")
    #         code = f"{shortuuid.uuid()}-{yr}"
    #         instance.email = f"{instance.email}_deleted_{code}"
    #         instance.is_active = False
    #         instance.save()
    #     else:
    #         raise PermissionDenied()

    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path="reset-password")
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            send_password_reset(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path="reset-password-confirm")
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if djoser_settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            djoser_settings.EMAIL.password_changed_confirmation(
                self.request, context
            ).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(method="GET", responses={200: UserSerializer})
    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
