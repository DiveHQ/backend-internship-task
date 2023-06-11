import requests
import json

url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'

def get_calories(query):
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': '1d730cb7',
        'x-app-key': '8ec54039f5f55a93bcbd9b13e949833a'
    }

    payload = {
        'query': query
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data = response.json()
        calories = data['foods'][0]['nf_calories']
        if isinstance('calories', int):
            return calories
    return 0
    

# get_calories('Plantain')
