import requests
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


def get_calories_from_api(text, API_KEY=settings.API_KEY):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = text
    print(API_KEY)
    response = requests.get(api_url + query, headers={'X-Api-Key': settings.API_KEY})
    
    if response.status_code == requests.codes.ok:
        response_data = response.json()  # Parse the response as JSON
        try:
            total_calories = sum(item['calories'] for item in response_data['items'])
            return int(total_calories)
        except:
            return Response({'detail': 'Error fetching data from API'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Error fetching data from API'}, status=status.HTTP_400_BAD_REQUEST)
