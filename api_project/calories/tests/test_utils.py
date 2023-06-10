from unittest.mock import MagicMock, patch

import pytest  # noqa

from api_project.calories.utils import get_calories_from_meal, sum_calories

test_list = [
    {
        "name": "salad",
        "calories": 15,
    },
    {
        "name": "beef burger",
        "calories": 35,
    },
]


test_res = {
    "items": [
        {
            "name": "salad",
            "calories": 50,
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
            "calories": 200,
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


def test_sum_calories():
    res = sum_calories(test_list)
    assert res == 50


@patch("api_project.calories.utils.requests")
def test_get_calories_from_meal(request_mock):
    mock_res = MagicMock()
    mock_res.status_code = 200
    mock_res.json.return_value = test_res

    request_mock.get.return_value = mock_res

    res = get_calories_from_meal("burger")
    assert res == 250
