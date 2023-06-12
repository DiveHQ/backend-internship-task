import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from tracker.models import Entry

User = get_user_model()


@pytest.mark.django_db
class TestEntry:
    """Test the Entry model."""

    def test_entry_creation(self):
        """Test that an Entry instance is created properly."""
        user = baker.make(User)

        entry = Entry.objects.create(
            user=user, text="Test Entry", calories=500, is_below_daily_calories_threshold=False
        )

        assert entry.user == user
        assert entry.text == "Test Entry"
        assert entry.calories == 500
        assert entry.is_below_daily_calories_threshold is False

    def test_entry_str_representation(self):
        """Test the __str__ method of Entry."""
        user = baker.make(User)

        entry = Entry.objects.create(
            user=user, text="Test Entry", calories=500, is_below_daily_calories_threshold=False
        )

        assert str(entry) == "Test Entry"
