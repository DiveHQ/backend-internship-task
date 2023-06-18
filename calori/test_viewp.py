from django.test import TestCase

class ViewTestCase(TestCase):
    def test_get(self):
        response= self.client.get('http://localhost:8000/project',data=None,headers={
            "Authorization":"Token ba53a1282b51f09da29d75f5d12b713a5a841db4a13dffc116d765f81f8002b6",
})
        print(response)

    def test_post(self):
        
        data ={
    "name": "egg",
    "quantity": 7,
    "calories": 300  
    }
        
        response = self.client.post("http://localhost:8000/project",data=data,headers={
            "Authorization":"Token ba53a1282b51f09da29d75f5d12b713a5a841db4a13dffc116d765f81f8002b6"
        })
        self.assertEqual(response.status_code,401)
    def test_delete(self):
        
        response = self.client.delete("http://localhost:8000/project/1",headers={
            "Authorization":"Token ba53a1282b51f09da29d75f5d12b713a5a841db4a13dffc116d765f81f8002b6"
        })
        self.assertEqual(response.status_code,401)
        
    def test_patch(self):
        data={
    "name": "egg",
    "quantity": 7,
    "calories": 300
    }
        
        response = self.client.patch("http://localhost:8000/project/1",data=data,headers={
            "Authorization":"Token ba53a1282b51f09da29d75f5d12b713a5a841db4a13dffc116d765f81f8002b6"
        })
        self.assertEqual(response.status_code, 401)