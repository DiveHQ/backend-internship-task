from datetime import date

import pytest
from accounts.models import UserSettings
from accounts.tests.conftest import UNAUTHORIZED_RESPONSE_MESSAGE
from core.constants import User
from model_bakery import baker
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from tracker.models import Entry

from .conftest import ENTRIES_LIST_URL, NO_CALORIES_FOR_QUERY_MESSAGE, entry_detail_url


@pytest.mark.django_db
class TestCreateEntry:
    """Test the create entry endpoint."""

    def test_any_user_can_create_an_entry_201(self, client: APIClient, entry_payload, sample_user):
        """Test that any user can create an entry."""
        client.force_authenticate(sample_user)

        response: Response = client.post(ENTRIES_LIST_URL, entry_payload)

        created_entry: Entry = Entry.objects.get(text=entry_payload["text"])
        assert response.status_code == status.HTTP_201_CREATED
        assert created_entry.calories == entry_payload["calories"]
        assert created_entry.user == sample_user
        assert created_entry.date == date.today()
        assert created_entry.below_daily_threshold

    def test_calories_are_retrieved_from_provider_if_blank_201(
        self, client: APIClient, entry_payload, mock_calories_provider, sample_user
    ):
        """Test that calories are retrieved from the calories provider if blank."""
        expected_calories = mock_calories_provider(status_code=200)
        client.force_authenticate(sample_user)
        del entry_payload["calories"]

        response: Response = client.post(ENTRIES_LIST_URL, entry_payload)

        created_entry: Entry = Entry.objects.get(text=entry_payload["text"])
        assert response.status_code == status.HTTP_201_CREATED
        assert created_entry.calories == expected_calories
        assert created_entry.user == sample_user
        assert created_entry.date == date.today()
        assert created_entry.below_daily_threshold

    def test_error_if_calories_provider_cannot_retrieve_calories_400(
        self, client: APIClient, entry_payload, mock_calories_provider, sample_user
    ):
        """
        Test that an error is returned if the calories provider cannot get calories for
        entered meal.
        """
        meal_not_found_error_code = 404
        mock_calories_provider(status_code=meal_not_found_error_code)
        client.force_authenticate(sample_user)
        del entry_payload["calories"]

        response: Response = client.post(ENTRIES_LIST_URL, entry_payload)

        exists = Entry.objects.filter(text=entry_payload["text"]).exists()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["text"] == [NO_CALORIES_FOR_QUERY_MESSAGE]
        assert not exists

    def test_calories_set_to_none_if_cannot_connect_to_provider(
        self, client: APIClient, entry_payload, mock_calories_provider, sample_user
    ):
        """
        Test that the calories for the entry are set to None when the calories
        provider cannot be connected to.
        """
        # As at now, anything apart from 200 or 404 would suffice.
        connection_failed_error_code = 401

        mock_calories_provider(status_code=connection_failed_error_code)
        client.force_authenticate(sample_user)
        del entry_payload["calories"]

        response: Response = client.post(ENTRIES_LIST_URL, entry_payload)

        created_entry: Entry = Entry.objects.get(text=entry_payload["text"])
        assert response.status_code == status.HTTP_201_CREATED
        assert created_entry.calories is None
        assert created_entry.user == sample_user
        assert created_entry.date == date.today()
        assert created_entry.below_daily_threshold

    def test_sets_below_daily_threshold_correctly_201(
        self, client: APIClient, sample_user: User, entry_payload
    ):
        """
        Test that the below_daily_threshold is set to False when the
        latest entry equals or exceeds the daily threshold.
        """
        baker.make(UserSettings, user=sample_user)
        expected_daily_calories = sample_user.settings.expected_daily_calories
        entry_payload.update({"calories": expected_daily_calories})
        client.force_authenticate(sample_user)

        response: Response = client.post(ENTRIES_LIST_URL, entry_payload)

        created_entry: Entry = Entry.objects.get(text=entry_payload["text"])
        assert response.status_code == status.HTTP_201_CREATED
        assert not created_entry.below_daily_threshold

    def test_anonymous_user_cannot_create_an_entry_401(self, client, entry_payload):
        """Test that anonymous user's cannot create an entry."""
        response: Response = client.post(ENTRIES_LIST_URL, entry_payload)

        created = Entry.objects.filter(text=entry_payload["text"]).exists()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not created


@pytest.mark.django_db
class TestListEntries:
    """Test the list entries endpoint."""

    def test_a_regular_user_can_list_only_their_entries_200(self, client: APIClient, sample_user):
        """Test that a regular user can list only their entries."""
        client.force_authenticate(sample_user)

        # Make other entries for a random user
        baker.make(Entry, user=baker.make(User), _quantity=3)

        # Make some entries for sample_user
        expected_list_count = 2
        baker.make(Entry, user=sample_user, _quantity=expected_list_count)

        response: Response = client.get(ENTRIES_LIST_URL)

        data = response.data
        assert response.status_code == status.HTTP_200_OK

        # Assert paginated list response
        assert data["count"] == expected_list_count
        assert len(data["results"]) == expected_list_count
        assert "next" in data
        assert "previous" in data

    def test_a_user_manager_can_list_only_their_entries_200(self, client: APIClient, user_manager):
        """Test that a user manager can list only their entries."""
        client.force_authenticate(user_manager)

        # Make other entries for a random user
        baker.make(Entry, user=baker.make(User), _quantity=3)

        # Make some entries for user_manager
        expected_list_count = 2
        baker.make(Entry, user=user_manager, _quantity=expected_list_count)

        response: Response = client.get(ENTRIES_LIST_URL)

        data = response.data
        assert response.status_code == status.HTTP_200_OK

        # Assert paginated list response
        assert data["count"] == expected_list_count
        assert len(data["results"]) == expected_list_count
        assert "next" in data
        assert "previous" in data

    def test_an_admin_can_list_all_entries_200(self, client: APIClient, admin_user, sample_user):
        """Test that an admin can list all entries."""
        client.force_authenticate(admin_user)

        # Make some entries for sample_user
        baker.make(Entry, user=sample_user, _quantity=3)
        expected_list_count = Entry.objects.count()

        response: Response = client.get(ENTRIES_LIST_URL)

        data = response.data
        assert response.status_code == status.HTTP_200_OK

        # Assert paginated list response
        assert data["count"] == expected_list_count
        assert len(data["results"]) == expected_list_count
        assert "next" in data
        assert "previous" in data

    def test_an_anonymous_user_cannot_list_entries_401(self, client: APIClient):
        """Test that an admin can list all entries."""
        baker.make(Entry, _quantity=3)

        response: Response = client.get(ENTRIES_LIST_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == {"detail": UNAUTHORIZED_RESPONSE_MESSAGE}


@pytest.mark.django_db
class TestUpdateEntry:
    """Test the update entry endpoint."""

    def test_any_user_can_update_his_entry_200(
        self, client: APIClient, entry_payload, sample_entry: Entry, sample_user
    ):
        """Test that any user can update his entry."""
        client.force_authenticate(sample_user)
        url = entry_detail_url(sample_entry.id)

        response: Response = client.put(url, entry_payload)

        sample_entry.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert sample_entry.calories == entry_payload["calories"]
        assert sample_entry.user == sample_user
        assert sample_entry.below_daily_threshold

    def test_an_admin_can_update_another_users_entry_200(
        self, client: APIClient, admin_user, entry_payload, sample_entry: Entry, sample_user
    ):
        """Test that an admin can update another users entry."""
        client.force_authenticate(admin_user)
        url = entry_detail_url(sample_entry.id)

        response: Response = client.put(url, entry_payload)

        sample_entry.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert sample_entry.calories == entry_payload["calories"]
        assert sample_entry.user == sample_user
        assert sample_entry.below_daily_threshold

    def test_calories_are_retrieved_from_provider_if_blank_200(
        self,
        client: APIClient,
        entry_payload,
        mock_calories_provider,
        sample_entry: Entry,
        sample_user,
    ):
        """Test that calories are retrieved from the calories provider if blank."""
        expected_calories = mock_calories_provider(status_code=200)
        client.force_authenticate(sample_user)
        del entry_payload["calories"]
        url = entry_detail_url(sample_entry.id)

        response: Response = client.patch(url, entry_payload)

        sample_entry.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert sample_entry.calories == expected_calories
        assert sample_entry.user == sample_user
        assert sample_entry.below_daily_threshold

    def test_sets_below_daily_threshold_correctly_200(
        self, client: APIClient, entry_payload, sample_entry: Entry, sample_user
    ):
        """
        Test that the below_daily_threshold is set to False when the
        updated entry causes the daily entries to equal or exceed the daily threshold.
        """
        baker.make(UserSettings, user=sample_user)
        expected_daily_calories = sample_user.settings.expected_daily_calories
        entry_payload.update({"calories": expected_daily_calories})
        client.force_authenticate(sample_user)
        url = entry_detail_url(sample_entry.id)

        response: Response = client.patch(url, entry_payload)

        sample_entry.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert not sample_entry.below_daily_threshold

    def test_user_cannot_update_another_users_entry_404(
        self, client: APIClient, entry_payload, sample_entry: Entry
    ):
        """Test that a user cannot update another users entry."""
        other_user = baker.make(User)
        client.force_authenticate(other_user)
        url = entry_detail_url(sample_entry.id)
        old_entry = sample_entry

        response: Response = client.put(url, entry_payload)

        sample_entry.refresh_from_db()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert sample_entry.calories == old_entry.calories
        assert sample_entry.user == old_entry.user
        assert sample_entry.below_daily_threshold == old_entry.below_daily_threshold


@pytest.mark.django_db
class TestDeleteEntry:
    """Test the delete entry endpoint."""

    def test_any_user_can_delete_his_entry_200(
        self, client: APIClient, sample_entry: Entry, sample_user
    ):
        """Test that any user can delete his entry."""
        client.force_authenticate(sample_user)
        url = entry_detail_url(sample_entry.id)

        response: Response = client.delete(url)

        exists = Entry.objects.filter(pk=sample_entry.id).exists()
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not exists

    def test_an_admin_can_delete_another_users_entry_200(
        self, client: APIClient, admin_user, sample_entry: Entry
    ):
        """Test that an admin can delete another users entry."""
        client.force_authenticate(admin_user)
        url = entry_detail_url(sample_entry.id)

        response: Response = client.delete(url)

        exists = Entry.objects.filter(pk=sample_entry.id).exists()
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not exists

    def test_user_cannot_delete_another_users_entry(self, client: APIClient, sample_entry: Entry):
        """Test that a user cannot delete another users entry."""
        other_user = baker.make(User)
        client.force_authenticate(other_user)
        url = entry_detail_url(sample_entry.id)

        response: Response = client.delete(url)

        exists = Entry.objects.filter(pk=sample_entry.id).exists
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert exists
