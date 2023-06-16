from django.test import TestCase
from authen.views import RegisterAPI,LoginAPI,UserManger

# Create your tests here.

class ViewTesting(TestCase):
    
    def test_register(self):
        data={
            
        }
        
        response= self.client.post("")
        self.assertEqual(response.status_code,200)
        
    def test_login(self):
        data ={
            
        }
        response = self.client.post("")
        self.assertEqual(response.status_code,200)

class View_Manager_Test(TestCase):
    
    def test_GetUser(self):
        
        response = self.client.get("")
        self.assertEqual(response.status_code,200)

    def test_CreateUser(self):
        
        data={
            
        }
        response = self.client.post("")
        self.assertEqual(response.status_code,200)
        
    def test_UpdateUser(self):
        
        data={
            
        }
        response = self.client.patch("")
        self.assertEqual(response.status_code,200)
        
    def test_DeleteUser(self):
        
        data={
            
        }
        response = self.client.delete("")
        self.assertEqual(response.status_code,200)
        