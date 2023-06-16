from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username=models.CharField(max_length=100)
    email=models.EmailField( max_length=254)
    password = models.CharField(max_length=50)
    daily_Cola = models.IntegerField()
    