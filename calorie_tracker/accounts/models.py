from core.constants import User
from django.db import models


class UserSettings(models.Model):
    """Model for user settings."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="settings", verbose_name="user"
    )
    expected_daily_calories = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2250,
        help_text="The expected number of calories a user aims to consume in a day.",
    )

    class Meta:
        verbose_name_plural = "User Settings"

    def __str__(self) -> str:
        return str(self.user)
