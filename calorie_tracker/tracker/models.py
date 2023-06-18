from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    text = models.TextField()
    calories = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return f"Entry for {self.user.username} on {self.date}"
