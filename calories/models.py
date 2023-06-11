from django.db import models
from users.models import User
from calory_limit.models import CaloryLimit



class Calories(models.Model):
    text = models.CharField(max_length=200, null=False)
    calories = models.FloatField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    calory_limit = models.ForeignKey(CaloryLimit, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = 'Calories'

    def __str__(self) -> str:
        return self.text