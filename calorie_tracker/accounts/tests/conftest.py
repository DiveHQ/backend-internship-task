import secrets

import pytest
from django.urls import reverse

TOKEN_OBTAIN_PAIR_URL = reverse("accounts:token_obtain_pair")
TOKEN_REFRESH_URL = reverse("accounts:token_refresh")
USER_LIST_URL = reverse("accounts:user-list")

FAILED_LOGIN_ERROR_MESSAGE = "No active account found with the given credentials"
INVALID_TOKEN_ERROR_MESSAGE = "Token is invalid or expired"

UNAUTHORIZED_RESPONSE_MESSAGE = "Authentication credentials were not provided."
FORBIDDEN_ERROR_MESSAGE = "You do not have permission to perform this action."

WEAK_PASSWORD_ERROR_MESSAGES = [
    "This password is too short. It must contain at least 8 characters.",
    "This password is too common.",
    "This password is entirely numeric.",
]


def user_detail_url(user_id: int):
    """Return user detail url for given user id."""
    return reverse("accounts:user-detail", args=[user_id])


def update_user_password_url(user_id: int):
    """Return update user password url for given user id."""
    return reverse("accounts:user-update-password", args=[user_id])


@pytest.fixture
def random_token():
    """Return a random token."""
    return secrets.token_urlsafe(32)


@pytest.fixture
def user_payload():
    """Return a payload of sample user information."""
    return {
        "username": "sample_user",
        "password": "test_pass123",
        "first_name": "First name",
        "last_name": "Last name",
    }
