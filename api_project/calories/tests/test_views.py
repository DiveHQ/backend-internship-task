from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

calories_res = {
    "items": [
        {
            "name": "salad",
            "calories": 23.6,
            "serving_size_g": 100,
            "fat_total_g": 0.2,
            "fat_saturated_g": 0,
            "protein_g": 1.5,
            "sodium_mg": 36,
            "potassium_mg": 32,
            "cholesterol_mg": 0,
            "carbohydrates_total_g": 4.9,
            "fiber_g": 1.9,
            "sugar_g": 2.2,
        },
        {
            "name": "beef burger",
            "calories": 246.1,
            "serving_size_g": 100,
            "fat_total_g": 11.6,
            "fat_saturated_g": 4.7,
            "protein_g": 15.2,
            "sodium_mg": 346,
            "potassium_mg": 136,
            "cholesterol_mg": 54,
            "carbohydrates_total_g": 17.8,
            "fiber_g": 0,
            "sugar_g": 0,
        },
    ]
}


User = get_user_model()


@pytest.mark.django_db
class TestCaloriesViews:
    def test_list_calories(self, api_client_auth, calories_factory, user: User):
        url = reverse("api:calories-list")

        calories_factory.create_batch(3, user=user)

        client = api_client_auth(user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        # test pagination
        assert "results" in resp_data
        assert len(resp_data["results"]) == 3

    def test_list_calories_admin(
        self, api_client_auth, calories_factory, admin, user: User
    ):
        url = reverse("api:calories-list")
        calories_factory.create_batch(3, user=user)
        calories_factory.create_batch(2, user=admin)

        client = api_client_auth(admin)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        # test pagination
        assert "results" in resp_data
        assert len(resp_data["results"]) == 5

    def test_list_calories_manager(
        self, api_client_auth, calories_factory, manager, user: User
    ):
        url = reverse("api:calories-list")
        calories_factory.create_batch(3, user=user)

        client = api_client_auth(manager)
        resp = client.get(url)

        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_create_calories(self, api_client_auth, user_factory, user: User):
        url = reverse("api:calories-list")
        test_user = user_factory()
        data = {"user": test_user.id, "meal": "burger", "calories": 234}

        client = api_client_auth(user)
        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["user"] == str(user.id)
        assert resp_data["meal"] == data["meal"]
        assert resp_data["calories"] == data["calories"]

    def test_create_calories_admin(self, api_client_auth, admin: User, user: User):
        url = reverse("api:calories-list")
        data = {"user": user.id, "meal": "burger", "calories": 234}

        client = api_client_auth(admin)
        resp = client.post(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_201_CREATED
        assert resp_data["user"] == str(user.id)
        assert resp_data["meal"] == data["meal"]
        assert resp_data["calories"] == data["calories"]

    def test_create_calories_manager(self, api_client_auth, manager: User, user: User):
        url = reverse("api:calories-list")
        data = {"user": user.id, "meal": "burger", "calories": 234}

        client = api_client_auth(manager)
        resp = client.post(url, data=data)

        assert resp.status_code == status.HTTP_403_FORBIDDEN

    @patch("api_project.calories.utils.requests")
    def test_create_calories_without_calories(
        self, request_mock, api_client_auth, manager: User, user: User
    ):
        request_result = MagicMock()
        request_result.status_code = 200
        request_result.json.return_value = calories_res

        request_mock.get.return_value = request_result

        url = reverse("api:calories-list")
        data = {"user": user.id, "meal": "burger"}

        client = api_client_auth(user)
        resp = client.post(url, data=data)

        assert resp.status_code == status.HTTP_201_CREATED

    def test_read_calories(self, api_client_auth, calories_factory, user: User):
        calories = calories_factory(user=user)
        url = reverse("api:calories-detail", args=(calories.id,))

        client = api_client_auth(user)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["meal"] == calories.meal
        assert resp_data["calories"] == calories.calories

    def test_read_calories_admin(
        self, api_client_auth, calories_factory, admin, user: User
    ):
        calories = calories_factory(user=user)
        url = reverse("api:calories-detail", args=(calories.id,))

        client = api_client_auth(admin)
        resp = client.get(url)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["meal"] == calories.meal
        assert resp_data["calories"] == calories.calories

    def test_read_calories_manager(
        self, api_client_auth, calories_factory, manager, user: User
    ):
        calories = calories_factory(user=user)
        url = reverse("api:calories-detail", args=(calories.id,))

        client = api_client_auth(manager)
        resp = client.get(url)

        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_update_calories(self, api_client_auth, calories_factory, user: User):
        calories = calories_factory(user=user)
        url = reverse("api:calories-detail", args=(calories.id,))
        data = {"calories": 23}

        client = api_client_auth(user)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["calories"] == data["calories"]

    def test_update_calories_admin(
        self, api_client_auth, calories_factory, admin: User, user: User
    ):
        calories = calories_factory(user=user)
        url = reverse("api:calories-detail", args=(calories.id,))
        data = {"calories": 23}

        client = api_client_auth(admin)
        resp = client.patch(url, data=data)
        resp_data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert resp_data["calories"] == data["calories"]

    def test_update_calories_manager(
        self, api_client_auth, calories_factory, manager: User, user: User
    ):
        calories = calories_factory(user=user)
        url = reverse("api:calories-detail", args=(calories.id,))
        data = {"calories": 23}

        client = api_client_auth(manager)
        resp = client.patch(url, data=data)

        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user(self, api_client_auth, calories_factory, user: User):
        calories = calories_factory(user=user)
        url = reverse("api:calories-detail", args=(calories.id,))

        client = api_client_auth(user)
        resp = client.delete(url)

        resp.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_user_manager(
        self, api_client_auth, calories_factory, manager: User, user: User
    ):
        calories = calories_factory(user=user)
        url = reverse("api:calories-detail", args=(calories.id,))

        client = api_client_auth(manager)
        resp = client.delete(url)

        resp.status_code == status.HTTP_403_FORBIDDEN
