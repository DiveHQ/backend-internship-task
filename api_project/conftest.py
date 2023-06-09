import pytest

from api_project.users.models import User
from api_project.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture(autouse=True)
def api_client():
    from rest_framework.test import APIClient

    return APIClient(format="json")
