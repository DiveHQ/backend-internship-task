from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    text = models.TextField()
    calories = models.PositiveIntegerField(blank=True)
    is_calories_below_expected = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Calculate the total calories for the day
        total_calories = Entry.objects.filter(user=self.user, date=self.date).aggregate(
            total_calories=models.Sum("calories")
        )["total_calories"]

        # Update the is_calories_below_expected field
        self.is_calories_below_expected = total_calories > self.user.expected_calories

        # Call the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entry for {self.user.username} on {self.date}"
