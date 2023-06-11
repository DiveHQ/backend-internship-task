"""General Project Fixtures."""
import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker

User = get_user_model()


@pytest.fixture
def sample_user():
    """Return a sample user."""
    user = baker.make(User)

    # Set user's password as "password"
    user.set_password("password")
    user.save()

    return user
