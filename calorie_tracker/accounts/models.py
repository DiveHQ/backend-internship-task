from core.constants import User
from django.db import models


class UserSettings(models.Model):
    """Model for user settings."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    expected_daily_calories = models.PositiveIntegerField(default=2250)

    class Meta:
        verbose_name_plural = "User Settings"

    def __str__(self) -> str:
        return str(self.user)
