from django.test import TestCase
from calori.models import Calo
from authen.models import User
# Create your tests here.

class ModelTestCase(TestCase):
    def test_limit_reached(self):
        data = User.objects.create(
            username="Kofi",
            email= "eek@gmaii.com",
            password="iloves",
            daily_calo= 300
        )
        
        calo = Calo.objects.create(user_id=1,name='bread',quantity=20,calories=350)
        
        calo.user = data
        calo.save()
        data.save()
        limit = calo
        self.assertEquals(calo.limt_reach,True)
        
