from django.contrib.auth import get_user_model
from django.db import models

from api_project.common.models import BaseModel

User = get_user_model()


# Create your models here.
class Calories(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calries")
    meal = models.CharField(max_length=255)
    calories = models.PositiveIntegerField(default=0)
    note = models.CharField(max_length=255, blank=True)
    extra = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name}::{self.calories}"
