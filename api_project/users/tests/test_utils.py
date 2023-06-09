import pytest
from django.core import mail

from api_project.users import utils
from api_project.users.models import User

pytestmark = pytest.mark.django_db


def test_send_welcome_email(user: User):
    utils.send_welcome_email(user)
    assert len(mail.outbox) == 1


def test_send_password_reset_email(user: User):
    utils.send_password_reset(user)
    assert len(mail.outbox) == 1
