from django.db import models
from users.models import User

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    text = models.TextField()
    calories = models.IntegerField(blank=True, null=True)
    meets_calorie_expectation = models.BooleanField(default=True)