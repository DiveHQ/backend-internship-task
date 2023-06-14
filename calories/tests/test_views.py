from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User
from calory_limit.models import CaloryLimit
from ..models import Calories

class CaloryViewsTest(APITestCase):
    url = reverse('calory_view', args=[1])
    
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

        

        self.calory_limit = CaloryLimit.objects.create(
            calory_limit = 55,
            description = 'I am burning these',
            user = self.user
        )
    
    def test_view_with_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_with_unauthenticated_user(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
    
    def test_post_calory_view_success(self):
        data = {
            'text': 'Apple',
            'calories': 77
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       
    def test_get_calory_view_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
class GetCaloryDetailsView(APITestCase):
    get_details_url = reverse('calory_details_view', args=[1])

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

        

        self.calory_limit = CaloryLimit.objects.create(
            calory_limit = 55,
            description = 'I am burning these',
            user = self.user
        )

        self.calory = Calories.objects.create(
            text = 'Apple',
            calories = 55
        )
    def test_view_with_authenticated_user(self):
        response = self.client.get(self.get_details_url)
        self.assertEqual(response.status_code, 200)

    def test_view_with_unauthenticated_user(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.get_details_url)
        self.assertEqual(response.status_code, 200)

    def test_get_calory_details_view_success(self):
        response = self.client.get(self.get_details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
class GetCurrentCaloryDetailsView(APITestCase):
    url = reverse('todays_calory') 
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

            

        self.calory_limit = CaloryLimit.objects.create(
            calory_limit = 55,
            description = 'I am burning these',
            user = self.user
        )

        self.calory = Calories.objects.create(
            text = 'Apple',
            calories = 55
        )

    def test_get_todays_calory_success(self): 
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200) 
    
    def test_view_with_unauthenticated_user(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)


class EditDeleteCaloryTestView(APITestCase):
    url = reverse('edit_delete_calory', args=[1]) 
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

            

        self.calory_limit = CaloryLimit.objects.create(
            calory_limit = 55,
            description = 'I am burning these',
            user = self.user
        )

        self.calory = Calories.objects.create(
            text = 'Apple',
            calories = 55,
            calory_limit = self.calory_limit
        )
    
    def test_put_calory_success(self):
        data = {
            'text': 'Banana',
            'calories': 77
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_put_calory_invalid_request_body(self):
        data = {
            
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_delete_calory_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)

    def test_view_calory_fail_wrong_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)




