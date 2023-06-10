import pytest
from django.core import mail
from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api_project.users.models import User

pytestmark = pytest.mark.django_db


class TestUserView:
    def test_user_list(self, api_client_auth, user: User):
        url = reverse("api:users-list")
        client = api_client_auth(user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert "results" in resp_data

    def test_user_read(self, api_client_auth, user: User):
        url = reverse("api:users-detail", args=(user.id,))
        client = api_client_auth(user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["email"] == user.email
        assert resp_data["role"] == User.Roles.USER

    def test_user_read_admin(self, api_client_auth, user: User, admin: User):
        url = reverse("api:users-detail", args=(user.id,))
        client = api_client_auth(admin)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["email"] == user.email
        assert resp_data["role"] == User.Roles.USER

    def test_user_read_manager(self, api_client_auth, user: User, manager: User):
        url = reverse("api:users-detail", args=(user.id,))
        client = api_client_auth(manager)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["email"] == user.email
        assert resp_data["role"] == User.Roles.USER

    def test_user_update(self, api_client_auth, user: User):
        url = reverse("api:users-detail", args=(user.id,))
        client = api_client_auth(user)
        data = {"email": "a@a.com", "name": "Hello World"}

        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["name"] == data["name"]
        assert resp_data["email"] == data["email"]

    def test_user_update_manager(self, api_client_auth, user: User, manager: User):
        url = reverse("api:users-detail", args=(user.id,))
        client = api_client_auth(manager)
        data = {"email": "a@a.com", "name": "Hello World"}

        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["name"] == data["name"]
        assert resp_data["email"] == data["email"]

    def test_user_update_not_user(self, api_client_auth, user: User, manager: User):
        url = reverse("api:users-detail", args=(manager.id,))
        client = api_client_auth(user)
        data = {"email": "a@a.com", "name": "Hello World"}

        resp = client.patch(url, data=data)

        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_me(
        self,
        api_client_auth,
        user: User,
    ):
        url = reverse("api:users-me")
        client = api_client_auth(user)

        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["email"] == user.email


class TestAuthView:
    def test_login(self, api_client: APIClient, user: User, test_password):
        url = reverse("api:token-obtain")
        response = api_client.post(
            url, data={"email": user.email, "password": test_password}
        )

        assert response.status_code == status.HTTP_200_OK

    def test_login_with_wrong_credentials(
        self, api_client: APIClient, user: User, test_password
    ):
        url = reverse("api:token-obtain")
        response = api_client.post(
            url, data={"email": user.email, "password": "wrong_password"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_signup(self, api_client: APIClient, test_password, test_email):
        url = reverse("api:signup")
        data = {
            "email": test_email,
            "name": "test_name",
            "password": test_password,
            "password2": test_password,
        }
        response = api_client.post(url, data=data)
        resp_data = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert resp_data["role"] == User.Roles.USER

        assert len(mail.outbox) == 0

    def test_refresh_token(self, api_client: APIClient, user: User, token: dict):
        url = reverse("api:token-refresh")

        data = {"refresh": token["refresh"]}
        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_200_OK
