from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from app.permissions import ManagerEditDeletePermission, CaloryEditDeletePermission
from .serializers import CalorySerializer
from .models import CaloryLimit, Calories
from .nutritionix import get_calories

import datetime


class CaloryView(APIView):
    permission_classes = [IsAuthenticated]
    def get_limit(self, pk):
        try:
            return CaloryLimit.objects.get(id=pk)
        except CaloryLimit.DoesNotExist:
            raise Http404
        
    def validate_and_save(self, request, limit):
        serializer = CalorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        limit.present_calory_amount += request.data['calories']
        if limit.present_calory_amount >= limit.calory_limit:
            limit.exceeded_maximum = True
        limit.save()

        serializer.save(user=request.user, calory_limit=limit)
        return serializer.data
    
    def post(self, request, pk):
        limit = self.get_limit(pk)
        if 'calories' not in request.data:
            calories = get_calories(request.data['text'])
            request.data['calories'] = calories
        
        try:
            data = self.validate_and_save(request, limit)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = { 'error': str(e)}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        
        
    def get(self, request, pk):
        limit = self.get_limit(pk)
        calories = Calories.objects.filter(calory_limit=pk).all()
        serializer = CalorySerializer(calories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CaloryDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [CaloryEditDeletePermission | ManagerEditDeletePermission]
    queryset = Calories.objects.all()
    serializer_class = CalorySerializer


    
class GetCurrentCaloryDetails(APIView):
    permission_classes = [ManagerEditDeletePermission | IsAdminUser | IsAuthenticated]
    def get(self, request):
        current_date = datetime.date.today()
        calories_data = Calories.objects.filter(user=request.user, created_at__date=current_date)
        serializer = CalorySerializer(calories_data, many=True)
        total_calories = sum(calories['calories'] for calories in serializer.data)
        response = {
            'total': total_calories,
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)  

