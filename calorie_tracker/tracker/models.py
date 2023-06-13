from core.constants import User
from django.db import models


class Entry(models.Model):
    """Entry model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    calories = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    below_daily_threshold = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self) -> str:
        return self.text
