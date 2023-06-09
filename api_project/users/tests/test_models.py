import pytest

from api_project.users.models import User, UserManager
from api_project.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_string(user: User):
    assert str(user) == user.email


def test_email_must_be_set_validation():
    user_manager = UserManager()
    with pytest.raises(ValueError):
        user_manager.create_user(email=None)


def test_common_queryset_active(user):
    UserFactory.create_batch(2, is_active=False)

    assert User.objects.count() == 3
    assert User.objects.active().count() == 1
    assert User.objects.active().first() == user


def test_common_queryset_inactive():
    inactive_user = UserFactory(is_active=False)
    # is active by default
    UserFactory.create_batch(2)

    assert User.objects.count() == 3
    assert User.objects.inactive().count() == 1
    assert User.objects.inactive().first() == inactive_user


def test_common_queryset_activate():
    assert User.objects.count() == 0

    user = UserFactory(is_active=False)

    assert User.objects.count() == 1
    assert User.objects.active().count() == 0
    assert User.objects.inactive().count() == 1
    assert User.objects.inactive().first() == user

    user.activate()

    assert User.objects.count() == 1
    assert User.objects.active().count() == 1
    assert User.objects.inactive().count() == 0
    assert User.objects.active().first() == user


def test_common_queryset_deactivate():
    assert User.objects.count() == 0

    user = UserFactory()

    assert User.objects.count() == 1
    assert User.objects.active().count() == 1
    assert User.objects.inactive().count() == 0
    assert User.objects.active().first() == user

    user.deactivate()

    assert User.objects.count() == 1
    assert User.objects.active().count() == 0
    assert User.objects.inactive().count() == 1
    assert User.objects.inactive().first() == user
