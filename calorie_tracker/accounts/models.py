from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    ROLES = (
        ("admin", "Admin"),
        ("user_manager", "User Manager"),
        ("regular_user", "Regular User"),
    )

    role = models.CharField(max_length=20, choices=ROLES, default="regular_user")
    expected_calories = models.PositiveIntegerField(default=2000)

    # Add any additional fields you require (e.g., email, password)

    def __str__(self):
        return self.username
