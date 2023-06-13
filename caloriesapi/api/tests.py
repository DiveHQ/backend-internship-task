from django.test import TestCase, Client
from datetime import date
from .models import User, Calories
from django.contrib.auth.models import Group, User as AuthUser
from rest_framework import status
from .serializers import CaloriesSerializer, UserSerializer, GroupUpdateSerializer


class CaloriesAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword", max_calories=250
        )
        self.client.login(username="testuser", password="testpassword")

        self.admin = User.objects.create_superuser(
            username="adminuser", password="adminpassword"
        )

    def test_create_account(self):
        url = "/api/account/create/"
        data = {"username": "new_user", "password": "password", "max_calories": 250}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        url = "/api/login/"
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        url = "/api/users/"
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_groups(self):
        user = User.objects.create_user(username="testuser2", password="testpassword2")
        group = Group.objects.create(name="User Manager")
        url = f"/api/user/{user.id}"
        data = {"groups": ["User Manager"]}
        self.client.force_login(self.admin)
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_calorie_entry(self):
        url = "/api/entry/"
        data = {
            "date": str(date.today()),
            "time": "12:00:00",
            "text": "Lunch",
            "calories": 500,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_calorie_entry(self):
        entry = Calories.objects.create(
            user=self.user,
            date=date.today(),
            time="12:00:00",
            text="Lunch",
            calories=500,
        )
        url = f"/api/entry/{entry.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_calorie_entry(self):
        entry = Calories.objects.create(
            user=self.user,
            date=date.today(),
            time="12:00:00",
            text="Lunch",
            calories=500,
        )
        url = f"/api/entry/update/{entry.id}"
        data = {"calories": 600}
        response = self.client.put(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["calories"], 600)

    def test_delete_calorie_entry(self):
        entry = Calories.objects.create(
            user=self.user,
            date=date.today(),
            time="12:00:00",
            text="Lunch",
            calories=500,
        )
        url = f"/api/entry/delete/{entry.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_calorie_entries(self):
        url = "/api/entries/?page=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_calorie_entries_by_date(self):
        url = "/api/entries/date?date=2023-06-10"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_calorie_entries_by_status(self):
        url = "/api/entries/status?status=below"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
