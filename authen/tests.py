from django.test import TestCase
from authen.views import RegisterAPI,LoginAPI,UserManger
from authen.models import User
from django.contrib.auth.models import Group
# Create your tests here.

class ViewTesting(TestCase):
    
    def test_register(self):
        data={
                    "username":"elshaddai1",
                    "email":"el-shadd1@gmail.com",
                    "password":"Breakfast9"
                    ,"daily_calo":300
        }
        
        response= self.client.post("http://localhost:8000/register",data=data,header={
            "Content-Type":"application/json"
        })
        print(response.content)
        self.assertEqual(response.status_code,200)
        
    def test_login(self):
        """
        expected username is registerd email
        """
        user = User.objects.create_user(username="testuser",email="elshaddai@gmail.com",daily_calo=300,password="abc123")
        user.save()
        data ={
             "username": "elshaddai@gmail.com",
                "password": "abc123"
        }
        response = self.client.post("http://localhost:8000/api/login/",data=data)
        print(response.content)
        self.assertEqual(response.status_code,200)

