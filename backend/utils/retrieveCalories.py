import requests
from django.conf import settings
from django.core.exceptions import ValidationError

API_URL = settings.NUTRITIONIX["API_URL"]
HEADERS = settings.NUTRITIONIX["HEADERS"]


def retrieveCalories(query: str):
    """
    Attempt to retrieve and return the number of calories from the
    calories provider.
    Raises a Validation error if the calories provider cannot retrieve
    calories for the entered
    text/query. and returns None if there were any other issues.
    """
    payload = {"query": query}

    try:
        response = requests.post(API_URL, headers=HEADERS, data=payload)
    except requests.exceptions.RequestException:
        return None

    if response.status_code == 200:
        return _calculate_total_calories(response)

    if response.status_code == 404:
        raise ValidationError(
            {"text": "No calories could be obtained for text input."}
        )

    return None


def _calculate_total_calories(response: requests.Response):
    """Calculate total calories for all foods in Response."""
    data = response.json()
    foods = data.get("foods", [])

    calories = sum(food.get("nf_calories", 0) for food in foods)

    return calories
