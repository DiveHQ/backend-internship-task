from django.db import models

from django.contrib.auth.models import AbstractUser
# from .models import User

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    calorie_goal = models.IntegerField(default=2000)
    
class Entry(models.Model):
    # class Meta:
    #     app_label = 'tracker'
    user = models.ForeignKey('tracker.User', on_delete=models.CASCADE)
    manager = models.ForeignKey('tracker.User', on_delete=models.CASCADE, related_name='entries_managed', blank=True, null=True)
    date = models.DateField()
    meal = models.CharField(max_length=100)
    calories = models.IntegerField()