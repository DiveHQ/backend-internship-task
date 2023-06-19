from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Entry
from .serializer import EntrySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import requests

#API function to get calories
def get_calories(meal_name):
    #Replace 'YOUR_API_KEY' with the API KEY 
    api_key = 'YOUR_API_KEY'
    base_url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    params = {
        'api_key': api_key,
        'query': meal_name,
        'dataType': 'Foundation',
        'pageSize': 1
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'foods' in data and len(data['foods']) > 0:
            food = data['foods'][0]
            if 'foodNutrients' in food:
                nutrients = food['foodNutrients']
                for nutrient in nutrients:
                    #Only get the calories value
                    if nutrient['nutrientName'] == 'Energy' and nutrient['unitName'] == 'KCAL':
                        calories = nutrient['value']
                        return calories
    return None

# API function to check whether user goal is met 
@api_view(['GET'])
def check_calorie_goal(request, date):
    user = request.user
    try:
        entries = Entry.objects.filter(user=user, date=date)
        total_calories = entries.aggregate(Sum('calories'))['calories__sum'] or 0
        calorie_goal = user.calorie_goal
        if total_calories < calorie_goal:
            is_goal_met = True
        else:
            is_goal_met = False
        return Response({'is_goal_met': is_goal_met})
    except Entry.DoesNotExist:
        return Response({'is_goal_met': False})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_entry(request):
    serializer = EntrySerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if 'calories' not in request.data or not request.data['calories']:
            meal = request.data.get('meal')
            calories = get_calories(meal)  # Call the get_calories function to fetch calories
            request.data['calories'] = calories
        if user.is_manager:
            # Assign manager to the entry
            manager = user
            serializer.save(user=user, manager=manager)
        else:
            # User is not a manager, return 403 Forbidden
            return Response({'message': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_entry(request, pk):
    try:
        entry = Entry.objects.get(pk=pk)
    except Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if entry.user == request.user or (entry.manager == request.user and request.user.is_manager):
        serializer = EntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_entry(request, pk):
    try:
        entry = Entry.objects.get(pk=pk)
    except Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if entry.user == request.user or (entry.manager == request.user and request.user.is_manager):
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def get_entries(request):
    if request.user.is_manager:
        entries = Entry.objects.filter(manager=request.user)
    else:
        entries = Entry.objects.filter(user=request.user)
    
    # Check if the request wants JSON response (REST API)
    if request.accepted_renderer.format == 'json':
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)
    
    # Render the entries on an HTML page
    context = {
        'entries': entries
    }
    return render(request, 'entry_list.html', context)

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('entry-list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('entry-list')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')



    