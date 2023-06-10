from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from caloriesapi.settings import (
    NUTRTIONIX_API_URL,
    NUTRTIONIX_API_KEY,
    NUTRTIONIX_APP_ID,
    AUTH_USER_MODEL,
)
import requests


class Calories(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    text = models.CharField(max_length=250)
    calories = models.PositiveIntegerField(blank=True, null=True)
    is_below_expected = models.BooleanField(blank=True, null=True)

    def get_calories(self):
        if not self.calories:
            url = NUTRTIONIX_API_URL
            data = {"query": self.text}
            headers = {"x-app-id": NUTRTIONIX_APP_ID, "x-app-key": NUTRTIONIX_API_KEY}
            try:
                response = requests.post(url, json=data, headers=headers)
                self.calories = response["foods"].get("nf_calories", 0)
            except requests.exceptions.RequestException as e:
                self.calories = None

    def set_below_expected(self):
        self.is_below_expected = self.user.max_calories < self.calories


class User(AbstractUser):
    max_calories = models.PositiveIntegerField(blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="user_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="user_permissions"
    )
