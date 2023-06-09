"""
Module for all Form Tests.
"""
import pytest
from django.utils.translation import gettext_lazy as _

from api_project.users.forms import UserCreationForm
from api_project.users.models import User

pytestmark = pytest.mark.django_db


class TestUserCreationForm:
    """
    Test class for all tests related to the UserCreationForm
    """

    def test_email_validation_error_msg(self, user: User):
        """
        Tests UserCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing email cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "email": user.email,
                "password1": user.password,
                "password2": user.password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors
        assert form.errors["email"][0] == _("This email has already been taken.")
