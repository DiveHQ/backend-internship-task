import pytest
from django.urls import resolve, reverse

from api_project.users.models import User

pytestmark = pytest.mark.django_db


def test_user_detail(user: User):
    assert (
        reverse("api:users:users-detail", kwargs={"id": str(user.uuid)})
        == f"/api/users/{user.uuid}/"
    )
    assert resolve(f"/api/users/{user.uuid}/").view_name == "api:users:users-detail"


def test_user_list():
    assert reverse("api:users:users-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:users:users-list"


def test_user_me():
    assert reverse("api:users:users-me") == "/api/users/me/"
    assert resolve("/api/users/me/").view_name == "api:users:users-me"
