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
    
    def limit_reached(self,request):
            suppose_calo = User.objects.filter(id=request.user.id).get()
            if self.calories >= suppose_calo.daily_calo  :
                self.limt_reach == True
                return self.limt_reach 
            else:
                return self.limt_reach == False
    