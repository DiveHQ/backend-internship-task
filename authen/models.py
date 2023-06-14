from django.db import models

# Create your models here.

class User(models.Model):
    first_name= models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    password =models.CharField(max_length= 150)

    