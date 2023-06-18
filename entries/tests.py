from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from users.models import User
from entries.models import Entry
from .serializers import EntrySerializer

class CreateEntryViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email='admin@example.com', password='password123', is_admin=True)
        self.user_manager = User.objects.create_user(email='manager@example.com', password='password123', is_user_manager=True)
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)

    def test_create_entry_view(self):
        """
        Test the create entry view with valid data.
        - Ensure that the response status code is 201 CREATED.
        - Ensure that the response contains the created entry data.
        """
        url = reverse('create_entry')
        self.client.force_authenticate(user=self.user)
        #set expected_calories = 2000
        user = User.objects.get(id=self.user.id)
        user.expected_calories = 2000
        user.save()
        data = {
            'user_id': self.user.id,
            'time': '11:30:00',
            'date': '2021-01-01',
            'text': 'This is a test entry.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_entry_view_without_authentication(self):
        """
        Test the create entry view without authentication.
        - Ensure that the response status code is 401 UNAUTHORIZED.
        """
        url = reverse('create_entry')
        data = {
            'user_id': self.user.id,
            'time': '11:30:00',
            'date': '2021-01-01',
            'text': 'This is a test entry.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_entry_view_by_admin_user(self):
        """
        Test the create entry view by admin user.
        - Admin user should be able to create an entry for any user.
        """
        url = reverse('create_entry')
        self.client.force_authenticate(user=self.admin_user)
        #set expected_calories = 2000
        user = User.objects.get(id=self.user.id)
        user.expected_calories = 2000
        user.save()
        data = {
            'user_id': self.user.id,
            'time': '11:30:00',
            'date': '2021-01-01',
            'text': 'This is a test entry.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  

    def test_create_entry_view_by_user_manager(self):
        """
        Test the create entry view by user manager.
        - User manager should not be able to create an entry for any user but themselves.
        """
        url = reverse('create_entry')
        self.client.force_authenticate(user=self.user_manager)
        #set expected_calories = 2000
        user = User.objects.get(id=self.user.id)
        user.expected_calories = 2000
        user.save()
        data = {
            'user_id': self.user.id,
            'time': '11:30:00',
            'date': '2021-01-01',
            'text': 'This is a test entry.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

    def test_create_entry_view_without_setting_expected_calories(self): 
        """
        Test the create entry view without setting expected calories for the user.
        - Ensure that the response status code is 400 BAD REQUEST.
        """
        url = reverse('create_entry')
        self.client.force_authenticate(user=self.user)
        data = {
            'user_id': self.user.id,
            'time': '11:30:00',
            'date': '2021-01-01',
            'text': 'This is a test entry.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateEntryViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email='admin@example.com', password='password123', is_admin=True)
        self.user_manager = User.objects.create_user(email='manager@example.com', password='password123', is_user_manager=True)
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        #set expected_calories = 2000
        self.user.expected_calories = 2000
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.entry = Entry.objects.create(user=self.user, time='11:30:00', date='2021-01-01', text='This is a test entry.')

    def test_update_entry_view(self):
        """
        Test the update entry view with valid data.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains the updated 'title' value.
        """
        url = reverse('update_entry')
        self.client.force_authenticate(user=self.user)
        data = {
            'entry_id': self.entry.id,
            'date': '2021-01-01',
            'time': '11:30:00',
            'text': 'This is a test entry.'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_entry_view_by_another_user(self):
        """
        Test the update entry view by another user.
        - Ensure that the response status code is 403 FORBIDDEN.
        """
        entry = Entry.objects.create(user=self.user, time='11:30:00', date='2021-01-01', text='This is a test entry.')
        url = reverse('update_entry')
        another_user = User.objects.create_user(email='anotheruser@example.com', password='password123')
        self.client.force_authenticate(user=another_user)
        data = {
            'entry_id': entry.id,
            'date': '2021-01-01',
            'time': '11:30:00',
            'text': 'This is a test entry.'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_entry_view_without_authentication(self):
        """
        Test the update entry view without authentication.
        - Ensure that the response status code is 401 UNAUTHORIZED.
        """
        entry = Entry.objects.create(user=self.user, time='11:30:00', date='2021-01-01', text='This is a test entry.')
        url = reverse('update_entry')
        data = {
            'entry_id': entry.id,
            'date': '2021-01-01',
            'time': '11:30:00',
            'text': 'This is a test entry.'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_entry_view_entry_does_not_exist(self):
        """
        Test the update entry view when the entry does not exist.
        - Ensure that the response status code is 404 NOT FOUND.
        """
        url = reverse('update_entry')
        self.client.force_authenticate(user=self.user)
        data = {
            'entry_id': 999,  # Non-existing entry ID
            'date': '2021-01-01',
            'time': '11:30:00',
            'text': 'This is a test entry.'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteEntryViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email='admin@example.com', password='password123', is_admin=True)
        self.user_manager = User.objects.create_user(email='manager@example.com', password='password123', is_user_manager=True)
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        #set expected_calories = 2000
        self.user.expected_calories = 2000
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.entry = Entry.objects.create(user=self.user, time='11:30:00', date='2021-01-01', text='This is a test entry.')

    def test_delete_entry_view(self):
        """
        Test the delete entry view.
        - Ensure that the response status code is 204 NO CONTENT.
        """
        url = reverse('delete_entry')
        data = {
            'entry_id': self.entry.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_entry_view_by_another_user(self):
        """
        Test the delete entry view by another user.
        - Ensure that the response status code is 403 FORBIDDEN.
        """
        url = reverse('delete_entry')
        another_user = User.objects.create_user(email='anotheruser@example.com', password='password123')
        self.client.force_authenticate(user=another_user)
        data = {
            'entry_id': self.entry.id
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_entry_view_without_authentication(self):
        """
        Test the delete entry view without authentication.
        - Ensure that the response status code is 401 UNAUTHORIZED.
        """
        url = reverse('delete_entry',)
        data = {
            'entry_id': self.entry.id
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_entry_view_entry_does_not_exist(self):
        """
        Test the delete entry view when the entry does not exist.
        - Ensure that the response status code is 404 NOT FOUND.
        """
        url = reverse('delete_entry')
        self.client.force_authenticate(user=self.user)
        data = {
            'entry_id': 999,  # Non-existing entry ID
        }
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_entry_view_entry_id_not_provided(self):
        """
        Test the delete entry view when the entry ID is not provided.
        - Ensure that the response status code is 400 BAD REQUEST.
        """
        url = reverse('delete_entry')
        self.client.force_authenticate(user=self.user)
        data = {}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListEntriesViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(email='admin@example.com', password='password123', is_admin=True)
        self.user_manager = User.objects.create_user(email='manager@example.com', password='password123', is_user_manager=True)
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        #set expected_calories = 2000
        self.user.expected_calories = 2000
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.entry = Entry.objects.create(user=self.user, time='11:30:00', date='2021-01-01', text='This is a test entry.')

    def test_list_entries_view(self):
        """
        Test the list entries view.
        - Ensure that the response status code is 200 OK.
        - Ensure that the response contains the serialized list of entry objects.
        """
        url = reverse('list_entries')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        entries = Entry.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 

    def test_list_entries_view_without_authentication(self):
        """
        Test the list entries view without authentication.
        - Ensure that the response status code is 401 UNAUTHORIZED.
        """
        url = reverse('list_entries')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

