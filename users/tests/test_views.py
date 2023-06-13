from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from ..models import User


class RegistrationViewTest(APITestCase):
    url = reverse('register_user')
    
    def test_registration_view_success(self):
        data = {
            'email':'test@example.com',
            'first_name':'Test',
            'last_name':'User',
            'role':'Regular',
            'password':'testpassword',
            'password2':'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_registration_view_fail_different_password(self):
        data = {
            'email':'test@example.com',
            'first_name':'Test',
            'last_name':'User',
            'role':'Regular',
            'password':'testpassword',
            'password2':'testpassword22'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_registration_view_fail_missing_key(self):
        data = {
            'email':'test@example.com',
            'first_name':'Test',
            'role':'Regular',
            'password':'testpassword',
            'password2':'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_registration_view_fail_invalid_role(self):
        data = {
            'email':'test@example.com',
            'first_name':'Test',
            'role':'Teacher',
            'password':'testpassword',
            'password2':'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)



class UserDetailsViewTest(APITestCase):
    url = reverse('edit_user_details', args=[1])

    def setUp(self):
        self.user = User.objects.create(
            email='test33@example.com',
            first_name='Test',
            last_name='User',
            role='Regular'
        )
        self.user.set_password('testpassword')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_edit_user_view_success(self):
        data = {
            'email':'test444@example.com',
            'first_name':'Test',
            'last_name': 'User',
            'role':'Manager',
            'password':'testpassword',
            'password2':'testpassword'
        }
        response = self.client.put(self.url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'Manager')
        self.assertEqual(response.data['email'], 'test444@example.com')

    def test_edit_user_view_missing_field(self):
        data = {
            'email':'test444@example.com',
            'first_name':'Test',
            'last_name': 'User',
            'role':'Manager',
            'password2':'testpassword'
        }
        response = self.client.put(self.url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, 400)
        

class LoginViewTest(APITestCase):
    url = reverse('token_obtain_pair')

    def setUp(self):
        self.user = User.objects.create(
            email='test33@example.com',
            first_name='Test',
            last_name='User',
            role='Regular'
        )
        self.user.set_password('testpassword')
        self.user.save()

    def test_login_view_success(self):
        data = {
            'email': 'test33@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_view_fail_user_does_not_exist(self):
        data = {
            'email': 'user@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_login_view_fail_missing_key(self):
        data = {
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
