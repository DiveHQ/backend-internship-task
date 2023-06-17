from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from users.models import User


class UserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email='admin@example.com', password='password123', is_admin=True)
        self.user_manager = User.objects.create_user(email='manager@example.com', password='password123', is_user_manager=True)
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)

    def test_login_view(self):
        """
        Test the login view with valid credentials.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains a 'token' key.
        """
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_view_with_invalid_credentials(self):
        """
        Test the login view with invalid credentials.
        - Ensure that the response status code is 401 UNAUTHORIZED.
        - Ensure that the response contains a 'detail' key with value 'Invalid credentials'.
        """
        url = reverse('login')
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid credentials')

    def test_logout_view(self):
        """
        Test the logout view.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains a 'detail' key with value 'Logged out successfully'.
        """
        url = reverse('logout')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Logged out successfully')

    def test_register_user_view(self):
        """
        Test the register user view with valid data.
        - Ensure that the response status code is 201 CREATED.
        - Ensure that the response contains a 'token' key.
        """
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'password123',
            'full_name': 'New User',
            'phone_number': '1234567890'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_register_user_view_with_existing_email(self):
        """
        Test the register user view with an existing email.
        - Ensure that the response status code is 400 BAD REQUEST.
        - Ensure that the response contains an 'email' key indicating the email already exists.
        """
        url = reverse('register')
        data = {
            'email': 'testuser@example.com',
            'password': 'password123',
            'full_name': 'New User',
            'phone_number': '1234567890'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_delete_user_view(self):
        """
        Test the delete user view.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains a 'detail' key with value 'User deleted successfully'.
        """
        url = reverse('delete')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'User deleted successfully')

    def test_delete_user_view_without_authentication(self):
        """
        Test the delete user view without authentication.
        - Ensure that the response status code is 401 UNAUTHORIZED.
        """
        url = reverse('delete')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_view(self):
        """
        Test the update user view with valid data.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains the updated 'full_name' value.
        """
        url = reverse('update')
        self.client.force_authenticate(user=self.user)
        data = {
            'full_name': 'Updated Name',
            'phone_number': '9876543210'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Updated Name')

    def test_update_user_view_with_invalid_data(self):
        """
        Test the update user view with invalid data.
        - Ensure that the response status code is 400 BAD REQUEST.
        - Ensure that the response contains an 'email' key indicating the email already exists.
        """
        url = reverse('update')
        self.client.force_authenticate(user=self.user)
        data = {
            'email': self.admin_user.email,  # Cannot update email field with already existing email
            'phone_number': '9876543210'  
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_list_users_view_with_admin(self):
        """
        Test the list users view with an admin user.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains a non-empty list of users.
        """
        url = reverse('list_users')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_list_users_view_with_user_manager(self):
        """
        Test the list users view with a user manager.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains a non-empty list of users.
        """
        url = reverse('list_users')
        self.client.force_authenticate(user=self.user_manager)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_list_users_view_with_normal_user(self):
        """
        Test the list users view with a normal user.
        - Ensure that the response status code is 403 FORBIDDEN.
        """
        url = reverse('list_users')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_view_without_authentication(self):
        """
        Test the list users view without authentication.
        - Ensure that the response status code is 401 UNAUTHORIZED.
        """
        url = reverse('list_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_detail_view(self):
        """
        Test the user detail view.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains the correct email of the user.
        """
        url = reverse('get_user')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_user_detail_view_with_valid_user_id(self):
        """
        Test the user detail view with a valid user ID.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains the correct email of the user.
        """
        url = reverse('get_user')
        self.client.force_authenticate(user=self.user)
        data = {
            'id': self.user.id
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
