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
    limt_reach = models.BooleanField(default=False)
    
    def limit_reached(self):
        
        if not self.limt_reach:
            
            suppose_calo = self.user.objects.get(daily_Calo="daily_Calo")

            if self.calories >= suppose_calo  :
                self.limt_reach == True
                return self.limt_reach 
            else:
                return self.limt_reach == False
    