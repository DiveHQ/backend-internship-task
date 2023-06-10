import logging
from functools import reduce

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError

headers = {"content-type": "application/json", "X-Api-Key": settings.CALORIES_API}

url = settings.CALORIES_BASE_URL


def sum_calories(calories_list: list):
    """
    Sum all the calories from the api together

    Params: list
    Return: int

    """
    new_list = [round(float(item["calories"])) for item in calories_list]
    return reduce(lambda a, b: a + b, new_list)


def get_calories_from_meal(meal):
    """
    Calculates the calories in a meal

    Params:
        meal:str

    Retrns:
        calories:int
    """

    params = {"query": meal}
    try:
        res = requests.get(url, params=params, headers=headers)
    except Exception as e:
        logging.warning(e)
        raise ValidationError(e)

    if res.status_code == status.HTTP_200_OK:
        list_of_calories = res.json().get("items", [])
        return sum_calories(list_of_calories)

    raise ValidationError(res.json())
