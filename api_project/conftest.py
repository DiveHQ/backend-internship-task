import pytest
from pytest_factoryboy import register
from rest_framework_simplejwt.tokens import RefreshToken

from api_project.calories.tests.factories import CaloriesFactory
from api_project.users.models import User
from api_project.users.tests.factories import UserFactory

register(UserFactory)
register(CaloriesFactory)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def test_email():
    return "test@email.com"


@pytest.fixture()
def test_password():
    return "something-a-bit-serious"


@pytest.fixture
def user(test_password) -> User:
    return UserFactory(password=test_password)


@pytest.fixture
def manager(test_password) -> User:
    return UserFactory(role=User.Roles.MANAGER, password=test_password)


@pytest.fixture
def admin(test_password) -> User:
    return UserFactory(role=User.Roles.ADMIN, password=test_password)


@pytest.fixture
def token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@pytest.fixture(autouse=True)
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_client_auth(api_client):
    """
    login user
    """

    def make_auth(user: User):
        api_client.force_authenticate(user=user)
        return api_client

    return make_auth
