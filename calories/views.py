from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from app.permissions import CaloryEditDeletePermission
from .serializers import CalorySerializer, CaloryLimitSerializer
from .models import CaloryLimit, Calories

import datetime




class CaloryLimitView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CaloryLimitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        calory_limits = CaloryLimit.objects.filter(user=request.user).all()
        serializer = CaloryLimitSerializer(calory_limits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CaloryLimitDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [CaloryEditDeletePermission]
    queryset = CaloryLimit.objects.all()
    serializer_class = CaloryLimitSerializer


class CaloryView(APIView):
    permission_classes = [IsAuthenticated]
    def get_limit(self, pk):
        try:
            return CaloryLimit.objects.get(id=pk)
        except CaloryLimit.DoesNotExist:
            raise Http404
    
    def post(self, request, pk):
        limit = self.get_limit(pk)
        serializer = CalorySerializer(data=request.data)
        if serializer.is_valid():
            limit.present_calory_amount+= request.data['calories']
            if limit.present_calory_amount >= limit.calory_limit:
                limit.exceeded_maximum = True
            limit.save()
            serializer.save(user=request.user, calory_limit=limit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
        
    def get(self, request, pk):
        limit = self.get_limit(pk)
        calories = Calories.objects.filter(calory_limit=pk).all()
        serializer = CalorySerializer(calories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CaloryDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Calories.objects.all()
    serializer_class = CalorySerializer

    
class GetCurrentCaloryDetails(APIView):
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

