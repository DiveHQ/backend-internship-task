from datetime import date

from django.db.models import Sum
from rest_framework import serializers

from backend.users.models import User, UserSettings
from backend.utils import retrieveCalories

from .models import Entry


class EntrySerializer(serializers.ModelSerializer):
    """Serializer for Entry model."""

    class Meta:
        model = Entry
        fields = [
            "id",
            "text",
            "date",
            "time",
            "calories",
            "below_daily_threshold",
            "user",
        ]
        read_only_fields = [
            "below_daily_threshold",
            "user",
        ]

    def create(self, validated_data):
        """Create a new Entry instance and set below_daily_threshold."""
        instance = super().create(validated_data)
        return self._set_below_daily_threshold(instance)

    def update(self, instance, validated_data):
        """Update an existing Entry instance and set below_daily_threshold."""
        instance = super().update(instance, validated_data)
        return self._set_below_daily_threshold(instance)

    def validate(self, attrs):
        """Try to retrieve calories if not provided."""
        text = attrs.get("text")
        calories = attrs.get("calories", None) or retrieveCalories(query=text)
        attrs["calories"] = calories
        return attrs

    def _set_below_daily_threshold(self, entry: Entry):
        """Sets the boolean on the entry instance and returns it."""
        user = entry.user
        total_calories_for_today = self._get_total_calories_for_today(user)
        user_settings, _ = UserSettings.objects.get_or_create(user=user)
        entry.below_daily_threshold = (
            total_calories_for_today < user_settings.expected_daily_calories
        )
        entry.save()
        return entry

    def _get_total_calories_for_today(self, user: User):
        """Returns the total calories for today's entries of the given user."""
        user_entries_for_today = Entry.objects.filter(
            user=user, date=date.today()
        )
        total_calories_for_today = (
            user_entries_for_today.aggregate(Sum("calories"))["calories__sum"]
            or 0
        )
        return total_calories_for_today
