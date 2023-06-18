from django.db import models
from authen.models import User
# Create your models here.
class Calo(models.Model):
    
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    calories = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    limt_reach = models.BooleanField(default=True,editable=True)
    
    