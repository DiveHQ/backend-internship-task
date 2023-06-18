from django.test import TestCase

class View_Manager_Test(TestCase):
    
    def test_GetUser(self):
        
        response = self.client.get("http://127.0.0.1:8000/api/v1/manager/",header={
            'Authorization':"Token 3afa3d4cf6cda1ebed51c2fe27dc71dca4e652541d1bcf613eccc1622c73efc1"
        })
        self.assertEqual(response.status_code,401)
        
        

    def test_CreateUser(self):
        
        data={
                "username":"clint1",
                "email":"clint1@gmail.com",
                "password":"clintCLint",
                "daily_calo":300
            }
        
        response = self.client.post("http://127.0.0.1:8000/api/v1/manager/",header={
            'Authorization':"Token 6290a3af7a8cdaef4b705959d897c5f6a5f0c55ad414fad6587d1e4c5c04937a"
        })
        self.assertEqual(response.status_code,401)
        
    def test_UpdateUser(self):
        """
        the dataset require can be one or more of the existing
        data set to update
    
        """
        data={
            "daily_calo":200
        }
        response = self.client.patch("http://127.0.0.1:8000/api/v1/manager/5",header={
            'Authorization':"Token 6290a3af7a8cdaef4b705959d897c5f6a5f0c55ad414fad6587d1e4c5c04937a"
        })
        self.assertEqual(response.status_code,401)
        
    def test_DeleteUser(self):
        
        response = self.client.delete("localhost:8000/api/v1/manager/4",header={
            'Authorization':"Token 6290a3af7a8cdaef4b705959d897c5f6a5f0c55ad414fad6587d1e4c5c04937a"
        })
        self.assertEqual(response.status_code,401)
        