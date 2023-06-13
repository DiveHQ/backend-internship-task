from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User


class CaloryLimitViewsTest(APITestCase):
    url = reverse('calory_limit')

    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='Regular'
        )
        self.user.set_password('testpassword')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_view_with_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_with_unauthenticated_user(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
    
    def test_post_calory_limit_success(self):
        data = {
            'calory_limit': 55,
            'description': 'I will burn them' 
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['calory_limit'], 55.0)
        self.assertEqual(response.data['description'], 'I will burn them')
        self.assertEqual(response.data['exceeded_maximum'], False)
        
    def test_post_calory_limit_fail(self):
        data = {
            'description': 'I will burn them' 
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_calory_limit_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
