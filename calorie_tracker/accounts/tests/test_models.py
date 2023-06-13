import pytest
from accounts.models import UserSettings
from core.constants import User
from model_bakery import baker


@pytest.mark.django_db
class TestUserSettings:
    """Test the UserSettings model."""

    def test_user_settings_creation(self):
        """Test that a UserSettings instance is created properly."""
        user = baker.make(User)

        settings = UserSettings.objects.create(user=user, expected_daily_calories=2000)

        assert settings.user == user
        assert settings.expected_daily_calories == 2000

    def test_user_settings_str_representation(self):
        """Test the __str__ method of UserSettings."""
        user = baker.make(User)

        settings = UserSettings.objects.create(user=user, expected_daily_calories=2000)

        assert str(settings) == str(user)
