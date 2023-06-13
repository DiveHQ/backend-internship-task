from decimal import Decimal

import pytest
import requests
from django.urls import reverse
from model_bakery import baker
from tracker.models import Entry

ENTRIES_LIST_URL = reverse("tracker:entry-list")

NO_CALORIES_FOR_QUERY_MESSAGE = "No calories could be obtained for text input."


def entry_detail_url(user_id: int):
    """Return entry detail url for given entry id."""
    return reverse("tracker:entry-detail", args=[user_id])


@pytest.fixture
def entry_payload():
    """Return sample entry information as a payload."""
    return {
        "text": "A loaf of bread.",
        "calories": 500,
    }


@pytest.fixture
def sample_entry(sample_user):
    """Return a sample entry assigned to sample_user."""
    return baker.make(Entry, user=sample_user)


@pytest.fixture
def mock_calories_provider(mocker):
    """Fixture that mocks the response of requests.post."""

    def mock_response(status_code=200):
        """
        Mock requests.post to respond with the specified status_code and JSON dictionary,
        and return the expected total calories from the response.
        """
        mocker.patch.object(requests, "post")

        requests.post.return_value.status_code = status_code

        response_json = {
            "foods": [{"nf_calories": 100.10}, {"nf_calories": 200.35}, {"nf_calories": 50}]
        }
        requests.post.return_value.json.return_value = response_json

        expected_total_calories = 350.45  # 100.10 + 200.25 + 50
        total_calories = sum(food.get("nf_calories", 0) for food in response_json["foods"])
        assert total_calories == expected_total_calories

        return Decimal(str(expected_total_calories))

    return mock_response
