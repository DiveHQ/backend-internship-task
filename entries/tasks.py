from dotenv import load_dotenv
import requests
import os
from rest_framework.response import Response
from rest_framework import status

load_dotenv()
API_KEY = os.getenv('API_KEY')



def get_calories_from_api(text, API_KEY=API_KEY):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = text
    response = requests.get(api_url + query, headers={'X-Api-Key': API_KEY})
    
    if response.status_code == requests.codes.ok:
        response_data = response.json()  # Parse the response as JSON
        try:
            total_calories = sum(item['calories'] for item in response_data['items'])
            return int(total_calories)
        except:
            return Response({'detail': 'Error fetching data from API'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Error fetching data from API'}, status=status.HTTP_400_BAD_REQUEST)

