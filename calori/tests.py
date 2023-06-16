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
            daily_Calo= 300
        )
        
        calo = Calo.objects.create(user_id=1,name='bread',quantity=20,calories=350)
        
        calo.user = data
        calo.save()
        data.save()
        limit = calo
        self.assertEquals(calo.limt_reach,True)
        
class ViewTestCase(TestCase):
    def test_Get(self):
        
        reponse= self.client.get('')
        self.assertEqual(response.status_code,200)

    def test_post(self):
        
        data ={
            
        }
        
        response = self.client.post('')
        self.assertEqual(response.status_code,200)
    def test_delete(self):
        
        response = self.client.delete("")
        self.assertEqual(response.status_code,200)
        
    def test_patch(self):
        data={
            
        }
        
        response = self.client.patch('')
        self.assertEqual(response.status_code, 200)