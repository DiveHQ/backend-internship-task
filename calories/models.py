from django.db import models
from users.models import User

class CaloryLimit(models.Model):
    calory_limit = models.FloatField(null=False, blank=False)
    description = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exceeded_maximum = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    present_calory_amount = models.FloatField(null=True, default=0)

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = 'Calory Limit'

    def __str__(self) -> str:
        return self.description



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