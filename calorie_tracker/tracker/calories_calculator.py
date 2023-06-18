import requests


def get_calories(food_name):
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"

    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "Content-Type": "application/json",
        "x-app-id": "d44e5586",
        "x-app-key": "e15b8d4092236ee5ead78a07289d6fb4",
    }
    data = {"query": food_name}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        # Extract the calorie information from the response
        calories = result["foods"][0]["nf_calories"]
        return calories
    else:
        # Handle the error case appropriately
        return 1
