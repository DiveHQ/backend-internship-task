import pytest
from accounts.models import UserSettings
from accounts.tests.conftest import (
    SETTINGS_ALREADY_EXIST_MESSAGE,
    USER_SETTINGS_LIST_URL,
    user_settings_detail_url,
)
from core.constants import User
from django.contrib.auth.models import User as UserModel
from model_bakery import baker
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateUserSettings:
    """Test the create user settings endpoint."""

    def test_user_can_create_his_settings_201(
        self, client: APIClient, sample_user: UserModel, user_settings_payload: UserSettings
    ):
        """Test that users can create their settings."""
        client.force_authenticate(sample_user)
        expected_daily_calories = user_settings_payload["expected_daily_calories"]

        response: Response = client.post(USER_SETTINGS_LIST_URL, user_settings_payload)

        created_setting = UserSettings.objects.get(user=sample_user)
        assert response.status_code == status.HTTP_201_CREATED
        assert created_setting.expected_daily_calories == expected_daily_calories

    def test_error_on_settings_already_exist_400(
        self, client: APIClient, sample_user: UserModel, user_settings_payload: UserSettings
    ):
        """Test that an error is returned if settings already exist for the request user."""
        settings = baker.make(UserSettings, user=sample_user)
        client.force_authenticate(sample_user)
        old_settings = settings

        response: Response = client.post(USER_SETTINGS_LIST_URL, user_settings_payload)

        settings.refresh_from_db()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == SETTINGS_ALREADY_EXIST_MESSAGE

        # Assert that the already existing settings were not altered.
        assert old_settings.id == settings.id
        assert old_settings.user == settings.user
        assert old_settings.expected_daily_calories == settings.expected_daily_calories


@pytest.mark.django_db
class TestRetrieveUserSettings:
    """Test the retrieve user settings endpoint."""

    def test_user_can_retrieve_his_settings_200(self, client: APIClient, sample_user: UserModel):
        """Test that users can retrieve their settings."""
        client.force_authenticate(sample_user)
        settings = baker.make(UserSettings, user=sample_user)
        url = user_settings_detail_url(settings.id)

        response: Response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == settings.id
        assert response.data["user"] == settings.user.id
        assert response.data["expected_daily_calories"] == settings.expected_daily_calories

    def test_user_cannot_retrieve_other_users_settings_404(
        self, client: APIClient, sample_user: UserModel
    ):
        """Test that users cannot retrieve the settings of a different user."""
        settings = baker.make(UserSettings, user=sample_user)
        url = user_settings_detail_url(settings.id)
        other_user = baker.make(User)
        client.force_authenticate(other_user)

        # other_user tries to get sample_user's settings
        response: Response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {"detail": "Not found."}


@pytest.mark.django_db
class TestUpdateUserSettings:
    """Test the update user settings endpoint."""

    def test_user_can_update_his_settings_200(
        self, client: APIClient, sample_user: UserModel, user_settings_payload: UserSettings
    ):
        """Test that users can update their settings."""
        client.force_authenticate(sample_user)
        settings = baker.make(UserSettings, user=sample_user)
        url = user_settings_detail_url(settings.id)
        expected_daily_calories = user_settings_payload["expected_daily_calories"]
        old_settings = settings

        response: Response = client.patch(url, user_settings_payload)

        settings.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert settings.id == old_settings.id
        assert settings.user == old_settings.user
        assert settings.expected_daily_calories == expected_daily_calories

    def test_user_cannot_update_other_users_settings_404(
        self, client: APIClient, sample_user: UserModel, user_settings_payload: UserSettings
    ):
        """Test that users cannot update the settings of a different user."""
        settings = baker.make(UserSettings, user=sample_user)
        url = user_settings_detail_url(settings.id)
        other_user = baker.make(User)
        client.force_authenticate(other_user)
        old_settings = settings

        # other_user tries to update sample_user's settings
        response: Response = client.patch(url, user_settings_payload)

        settings.refresh_from_db()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {"detail": "Not found."}
        assert settings.id == old_settings.id
        assert settings.user == old_settings.user
        assert settings.expected_daily_calories == old_settings.expected_daily_calories
