import pytest
from accounts.tests.conftest import (
    FAILED_LOGIN_ERROR,
    INVALID_TOKEN_ERROR,
    TOKEN_OBTAIN_PAIR_URL,
    TOKEN_REFRESH_URL,
)
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import DjangoClient


@pytest.mark.django_db
class TestTokenObtainPair:
    """Test the obtain token pair endpoint."""

    def test_return_access_and_refresh_tokens_200(self, client: DjangoClient, sample_user: User):
        """Test that valid credentials will return an access and refresh token."""

        payload = {
            "username": sample_user.username,
            "password": "password",
        }

        response: Response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_invalid_password_returns_401(self, client: DjangoClient, sample_user: User):
        """Test that an invalid password returns an error."""

        payload = {"username": sample_user.username, "password": "invalid_password"}

        response: Response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == FAILED_LOGIN_ERROR
        assert "access" not in response.data
        assert "refresh" not in response.data

    def test_invalid_username_returns_401(self, client: DjangoClient, sample_user: User):
        """Test that an invalid username returns an error."""

        payload = {"username": "invalid_username", "password": "password"}

        response: Response = client.post(TOKEN_OBTAIN_PAIR_URL, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == FAILED_LOGIN_ERROR
        assert "access" not in response.data
        assert "refresh" not in response.data


@pytest.mark.django_db
class TestTokenRefresh:
    """Test the token refresh endpoint."""

    def test_return_access_token_200(self, client: DjangoClient, sample_user: User):
        """Test that a valid refresh token will return a new access token."""

        user_credentials_payload = {"username": sample_user.username, "password": "password"}
        token_pair_response: Response = client.post(TOKEN_OBTAIN_PAIR_URL, user_credentials_payload)
        refresh_token = token_pair_response.data["refresh"]
        payload = {"refresh": refresh_token}

        response: Response = client.post(TOKEN_REFRESH_URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_invalid_refresh_returns_401(self, client: DjangoClient, sample_user, random_token):
        """Test that an invalid refresh token returns an error."""

        payload = {"refresh": random_token}

        response: Response = client.post(TOKEN_REFRESH_URL, payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == INVALID_TOKEN_ERROR
        assert "access" not in response.data
