from django.db import models

# Create your models here.
from backend.users.models import User


class Entry(models.Model):
    """Entry model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="entries",
        help_text="The user associated with this entry",
    )
    text = models.TextField(
        help_text=(
            "The description of the meal(s) taken. "
            "Please prefix each meal with the quantity of any measurement."
        )
    )
    date = models.DateField(
        auto_now_add=True, help_text="The date of the entry"
    )
    time = models.TimeField(
        auto_now_add=True, help_text="The time of the entry"
    )
    calories = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="The number of calories in the meal(s)",
    )
    below_daily_threshold = models.BooleanField(
        default=True,
        help_text=(
            "Indicates if this entry causes the assigned user's total calories for the day "
            "to be equal to or exceed their expected daily calories"
        ),
    )

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self) -> str:
        return self.text
