from django.db import models

# Create your models here.

"""class User(models.Model):
    first_name= models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100 )
    email = models.EmailField(max_length=150, unique=True)
    password =models.CharField(max_length= 150 )
"""
    
"""
Calories Model
"""

class Calo(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.IntegerField(max_length=5)
    Calories = models.IntegerField(max_length=5)
    date_time = models.DateTimeField()