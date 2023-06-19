

import requests
from config import Config

def get_calories_from_nutritionix_api(query):
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': 'd8ffd5b5',
        'x-app-key': '026b80636b4948cd0dbaedf8d73a261f'
    }
    body = {
        'query': query,
        'timezone': 'US/Eastern'
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    return calories
