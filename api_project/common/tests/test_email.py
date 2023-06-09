import pytest
from django.core import mail

from api_project.common.email import send_email
from api_project.users.models import User

pytestmark = pytest.mark.django_db


def test_send_email(user: User):
    send_email(user, "template-id", {"name": "jeff"})
    assert len(mail.outbox) == 1
