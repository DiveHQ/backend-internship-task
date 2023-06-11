import secrets

import pytest
from django.urls import reverse

TOKEN_OBTAIN_PAIR_URL = reverse("accounts:token_obtain_pair")
TOKEN_REFRESH_URL = reverse("accounts:token_refresh")

FAILED_LOGIN_ERROR = "No active account found with the given credentials"
INVALID_TOKEN_ERROR = "Token is invalid or expired"


@pytest.fixture
def random_token():
    """Return a random token."""
    return secrets.token_urlsafe(32)
