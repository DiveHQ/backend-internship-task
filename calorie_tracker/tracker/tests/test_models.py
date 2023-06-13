import pytest
from core.constants import User
from model_bakery import baker
from tracker.models import Entry


@pytest.mark.django_db
class TestEntry:
    """Test the Entry model."""

    def test_entry_creation(self, entry_payload):
        """Test that an Entry instance is created properly."""
        user = baker.make(User)

        entry = Entry.objects.create(user=user, **entry_payload)

        assert entry.user == user
        assert entry.text == entry_payload["text"]
        assert entry.calories == entry_payload["calories"]
        assert entry.below_daily_threshold

    def test_entry_str_representation(self, entry_payload):
        """Test the __str__ method of Entry."""
        user = baker.make(User)

        entry = Entry.objects.create(user=user, **entry_payload)

        assert str(entry) == entry_payload["text"]
