import pytest
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import RequestFactory
from django.urls.base import reverse
from pytest_django import asserts as pytest_django_asserts
from rest_framework import status
from rest_framework.test import APIClient

from api_project.common.utils import encode_uid
from api_project.users.models import User
from api_project.users.views import CustomDjoserViewSet, UserViewSet

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "uuid": str(user.uuid),
            "email": user.email,
            "name": user.name,
        }


class TestCustomDjoserViewSet:
    def test_me(self, user: User, rf: RequestFactory):
        view = CustomDjoserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)
        assert response.data == {
            "uuid": str(user.uuid),
            "email": user.email,
            "name": user.name,
        }

    def test_send_reset_password_email(self, api_client: APIClient, user: User):
        url = reverse("api:users:users-reset-password")
        response = api_client.post(url, data={"email": user.email})

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(mail.outbox) == 1

    def test_should_not_send_reset_password_email_if_user_does_not_exist(
        self, api_client: APIClient
    ):
        url = reverse("api:users:users-reset-password")
        data = {"email": "nothing"}
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # pytest django exports the regular unittest assertion methods as well as django's
        # https://docs.python.org/3/library/unittest.html#assert-methods
        # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#assertions
        pytest_django_asserts.assertContains(
            response,
            "Enter a valid email address",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        assert len(mail.outbox) == 0

    def test_reset_password_confirmation(self, api_client: APIClient, user: User):
        url = reverse("api:users:users-reset-password-confirm")

        data = {
            "uid": encode_uid(user.pk),
            "token": default_token_generator.make_token(user),
            "new_password": "new password",
        }
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(mail.outbox) == 1
