"""General Project Fixtures."""
import pytest
from accounts.constants import USER_MANAGER_GROUP
from core.constants import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as UserModel
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def sample_user():
    """Return a sample user."""
    user = baker.make(User, is_active=True, is_staff=False, is_superuser=False)

    # Set user's password as "password"
    user.set_password("password")
    user.save()

    return user


@pytest.fixture
def user_manager():
    """Return a user in the User Managers group."""
    group = Group.objects.get(name=USER_MANAGER_GROUP)
    user: UserModel = baker.make(User)
    user.groups.add(group)

    return user


@pytest.fixture
def admin_user():
    """Return an admin user."""
    return baker.make(User, is_staff=True)


@pytest.fixture
def client():
    """Return an api client."""
    return APIClient()
