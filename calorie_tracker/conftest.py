"""General Project Fixtures."""
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def sample_user():
    """Return a sample user."""
    user = baker.make(User, is_active=True, is_staff=False, is_superuser=False)

    # Set user's password as "password"
    user.set_password("password")
    user.save()

    return user


@pytest.fixture
def client():
    """Return an api client."""
    return APIClient()
