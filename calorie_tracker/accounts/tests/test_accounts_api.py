import pytest
from accounts.tests.conftest import (
    FAILED_LOGIN_ERROR_MESSAGE,
    FORBIDDEN_ERROR_MESSAGE,
    INVALID_TOKEN_ERROR_MESSAGE,
    TOKEN_OBTAIN_PAIR_URL,
    TOKEN_REFRESH_URL,
    USER_LIST_URL,
    WEAK_PASSWORD_ERROR_MESSAGES,
    update_user_password_url,
    user_detail_url,
)
from core.constants import User
from django.contrib.auth.models import User as UserModel
from model_bakery import baker
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestTokenObtainPair:
    """Test the obtain token pair endpoint."""

    def test_return_access_and_refresh_tokens_200(self, client: APIClient, sample_user: UserModel):
        """Test that valid credentials will return an access and refresh token."""

        payload = {
            "username": sample_user.username,
            "password": "password",
        }

        response: Response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_invalid_password_returns_401(self, client: APIClient, sample_user: UserModel):
        """Test that an invalid password returns an error."""

        payload = {"username": sample_user.username, "password": "invalid_password"}

        response: Response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == FAILED_LOGIN_ERROR_MESSAGE
        assert "access" not in response.data
        assert "refresh" not in response.data

    def test_invalid_username_returns_401(self, client: APIClient, sample_user: UserModel):
        """Test that an invalid username returns an error."""

        payload = {"username": "invalid_username", "password": "password"}

        response: Response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == FAILED_LOGIN_ERROR_MESSAGE
        assert "access" not in response.data
        assert "refresh" not in response.data


@pytest.mark.django_db
class TestTokenRefresh:
    """Test the token refresh endpoint."""

    def test_return_access_token_200(self, client: APIClient, sample_user: UserModel):
        """Test that a valid refresh token will return a new access token."""

        user_credentials_payload = {"username": sample_user.username, "password": "password"}
        token_pair_response: Response = client.post(TOKEN_OBTAIN_PAIR_URL, user_credentials_payload)
        refresh_token = token_pair_response.data["refresh"]
        payload = {"refresh": refresh_token}

        response: Response = client.post(TOKEN_REFRESH_URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_invalid_refresh_returns_401(self, client: APIClient, sample_user, random_token):
        """Test that an invalid refresh token returns an error."""

        payload = {"refresh": random_token}

        response: Response = client.post(TOKEN_REFRESH_URL, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == INVALID_TOKEN_ERROR_MESSAGE
        assert "access" not in response.data


@pytest.mark.django_db
class TestCreateUser:
    """Test the create user endpoint."""

    def _test_create_user(self, client: APIClient, authenticated_user, user_payload):
        """
        Helper function to test user creation by an authenticated user. This test is not meant
        to be run independently (starts with an underscore) and is used by other test cases.
        """
        client.force_authenticate(authenticated_user)

        response: Response = client.post(USER_LIST_URL, user_payload)

        created_user: UserModel = User.objects.get(username=user_payload["username"])
        assert response.status_code == status.HTTP_201_CREATED
        assert created_user.check_password(user_payload["password"])
        assert created_user.first_name == user_payload["first_name"]
        assert created_user.last_name == user_payload["last_name"]

    def test_user_manager_can_create_a_user_201(
        self, client: APIClient, user_manager, user_payload
    ):
        """Test that user managers can create users."""
        self._test_create_user(client, user_manager, user_payload)

    def test_an_admin_can_create_a_user_201(self, client: APIClient, admin_user, user_payload):
        """Test that an admin can create users."""
        self._test_create_user(client, admin_user, user_payload)

    def test_a_weak_password_returns_400(self, client: APIClient, user_manager, user_payload):
        """Test that creating a user with a weak password throws an error."""
        user_payload.update({"password": "123"})
        client.force_authenticate(user_manager)

        response: Response = client.post(USER_LIST_URL, user_payload)

        is_created = User.objects.filter(username=user_payload["username"]).exists()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["password"] == WEAK_PASSWORD_ERROR_MESSAGES
        assert not is_created

    def test_a_regular_user_cannot_create_a_user_403(
        self, client: APIClient, sample_user, user_payload
    ):
        """Test that regular users cannot create users."""

        client.force_authenticate(sample_user)

        response: Response = client.post(USER_LIST_URL, user_payload)

        is_created = User.objects.filter(username=user_payload["username"]).exists()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == FORBIDDEN_ERROR_MESSAGE
        assert not is_created


@pytest.mark.django_db
class TestListUsers:
    """Test the list users endpoint."""

    def _test_list_users(self, client: APIClient, authenticated_user):
        """
        Helper function to test listing users by an authenticated user. This test is not meant
        to be run independently (starts with an underscore) and is used by other test cases.
        """
        baker.make(User, _quantity=3)
        client.force_authenticate(authenticated_user)
        expected_user_count = User.objects.count()

        response: Response = client.get(USER_LIST_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == expected_user_count
        assert "next" in response.data
        assert "previous" in response.data
        users_listed = response.data["results"]
        assert len(users_listed) == expected_user_count

    def test_a_user_manager_can_list_users_200(self, client: APIClient, user_manager):
        """Test that user managers can list users."""
        self._test_list_users(client, user_manager)

    def test_an_admin_can_list_users_200(self, client: APIClient, admin_user):
        """Test that an admin can list users."""
        self._test_list_users(client, admin_user)

    def test_a_regular_user_cannot_list_users_403(self, client: APIClient, sample_user):
        """Test that regular users cannot list users."""

        client.force_authenticate(sample_user)

        response: Response = client.get(USER_LIST_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == FORBIDDEN_ERROR_MESSAGE


@pytest.mark.django_db
class TestUpdateUsers:
    """Test the update users endpoint."""

    def _test_update_user(
        self,
        client: APIClient,
        sample_user: UserModel,
        authenticated_user,
        user_payload,
        http_method,
    ):
        """
        Helper function to test updating a user by an authenticated user using the specified
        HTTP method. This test is not meant to be run independently (starts with an underscore)
        and is used by other test cases.
        """
        url = user_detail_url(sample_user.id)
        client.force_authenticate(authenticated_user)

        if http_method == "put":
            response: Response = client.put(url, user_payload)
        elif http_method == "patch":
            response: Response = client.patch(url, user_payload)
        else:
            raise ValueError("Invalid HTTP method specified.")

        sample_user.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert sample_user.check_password(user_payload["password"])
        assert sample_user.first_name == user_payload["first_name"]
        assert sample_user.last_name == user_payload["last_name"]

    def test_user_manager_put_updates_a_user_200(
        self, client: APIClient, sample_user: UserModel, user_manager, user_payload
    ):
        """Test that user managers can update users (PUT)."""
        self._test_update_user(client, sample_user, user_manager, user_payload, "put")

    def test_user_manager_patch_updates_a_user_200(
        self, client: APIClient, sample_user: UserModel, user_manager, user_payload
    ):
        """Test that user managers can update users (PATCH)."""
        self._test_update_user(client, sample_user, user_manager, user_payload, "patch")

    def test_admin_put_updates_a_user_200(
        self, client: APIClient, sample_user: UserModel, admin_user, user_payload
    ):
        """Test that admins can update users (PUT)."""
        self._test_update_user(client, sample_user, admin_user, user_payload, "put")

    def test_admin_patch_updates_a_user_200(
        self, client: APIClient, sample_user: UserModel, admin_user, user_payload
    ):
        """Test that admins can update users (PATCH)."""
        self._test_update_user(client, sample_user, admin_user, user_payload, "patch")

    def test_weak_password_returns_400(
        self, client: APIClient, sample_user, user_manager, user_payload
    ):
        """Test that updating a user with a weak password throws an error."""
        user_payload.update({"password": "123"})
        url = user_detail_url(sample_user.id)
        client.force_authenticate(user_manager)

        response: Response = client.patch(url, user_payload)

        is_updated = User.objects.filter(username=user_payload["username"]).exists()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["password"] == WEAK_PASSWORD_ERROR_MESSAGES
        assert not is_updated

    def test_a_regular_user_cannot_update_a_user_403(
        self, client: APIClient, sample_user: UserModel, user_payload
    ):
        """Test that regular users cannot update users."""
        url = user_detail_url(sample_user.id)
        client.force_authenticate(sample_user)

        response: Response = client.patch(url, user_payload)

        is_updated = User.objects.filter(username=user_payload["username"]).exists()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not is_updated

        response: Response = client.put(url, user_payload)

        is_updated = User.objects.filter(username=user_payload["username"]).exists()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not is_updated


@pytest.mark.django_db
class TestDeleteUsers:
    """Test the delete users endpoint."""

    def _test_delete_user(self, client: APIClient, sample_user: UserModel, authenticated_user):
        """
        Helper function to test deleting a user by an authenticated user. This test is not meant
        to be run independently (starts with an underscore) and is used by other test cases.
        """
        url = user_detail_url(sample_user.id)
        client.force_authenticate(authenticated_user)

        response: Response = client.delete(url)

        exists = User.objects.filter(pk=sample_user.id).exists()
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not exists

    def test_a_user_manager_can_delete_a_user_204(
        self, client: APIClient, sample_user: UserModel, user_manager
    ):
        """Test that user managers can delete users."""
        self._test_delete_user(client, sample_user, user_manager)

    def test_an_admin_can_delete_a_user_204(
        self, client: APIClient, sample_user: UserModel, admin_user
    ):
        """Test that admins can delete users."""
        self._test_delete_user(client, sample_user, admin_user)

    def test_a_regular_user_cannot_delete_users_403(
        self, client: APIClient, sample_user: UserModel
    ):
        """Test that regular users cannot delete users."""
        url = user_detail_url(sample_user.id)
        client.force_authenticate(sample_user)

        response: Response = client.delete(url)

        exists = User.objects.filter(pk=sample_user.id).exists()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert exists


@pytest.mark.django_db
class TestUpdateUserPassword:
    """Test the update user password endpoint."""

    def test_updates_the_request_users_password_200(
        self, client: APIClient, sample_user: UserModel, user_payload
    ):
        """Test that the request user's password is updated."""
        url = update_user_password_url(sample_user.id)
        client.force_authenticate(sample_user)

        response: Response = client.patch(url, user_payload)

        old_user = sample_user
        sample_user.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert sample_user.check_password(user_payload["password"])
        assert sample_user.first_name == old_user.first_name
        assert sample_user.last_name == old_user.last_name

    def test_users_cannot_update_other_users_passwords_403(
        self, client: APIClient, sample_user: UserModel, user_payload
    ):
        """Test that a user cannot update another user's password."""
        other_user: UserModel = baker.make(User)
        url = update_user_password_url(other_user.id)
        client.force_authenticate(sample_user)

        response: Response = client.patch(url, user_payload)

        other_user.refresh_from_db()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == FORBIDDEN_ERROR_MESSAGE
        assert not other_user.check_password(user_payload["password"])
