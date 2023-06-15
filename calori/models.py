from django.db import models

# Create your models here.

class Calo(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    calories = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
