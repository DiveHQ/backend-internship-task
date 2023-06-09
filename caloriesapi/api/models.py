from django.db import models
from django.contrib.auth.models import User


class Calories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    text = models.CharField(max_length=250)
    calories = models.PositiveIntegerField(blank=True, null=True)
    is_below_expected = models.BooleanField(blank=True, null=True)
    
    def get_calories(self):
        if not self.calories:
            pass
