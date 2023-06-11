from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from app.permissions import CaloryEditDeletePermission
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import CaloryLimitSerializer
from .models import CaloryLimit

# Create your views here.
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
