from core.constants import User
from django.db import models


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    calories = models.IntegerField(blank=True, null=True)
    is_below_daily_calories_threshold = models.BooleanField()

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self) -> str:
        return self.text
