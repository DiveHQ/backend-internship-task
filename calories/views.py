from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from app.permissions import ManagerEditDeletePermission, IsOwnerOrReadOnly
from calory_limit.serializers import CaloryLimitSerializer
from .serializers import CalorySerializer
from .models import CaloryLimit, Calories
from .nutritionix import get_calories

import datetime


class CaloryView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    This function gets an instance of the calory limit model
    '''
    def get_limit(self, pk):
        try:
            return CaloryLimit.objects.get(id=pk)
        except CaloryLimit.DoesNotExist:
            raise Http404
    
    '''
    This function is for validating and save into database,
    data for the calory model
    '''
    def validate_and_save(self, request, limit):
        serializer = CalorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        limit.present_calory_amount += request.data['calories']
        if limit.present_calory_amount >= limit.calory_limit:
            limit.exceeded_maximum = True
        limit.save()

        serializer.save(user=request.user, calory_limit=limit)
        return serializer.data
    
    '''
    A post request for creating a calory resource in the database
    '''
    def post(self, request, pk):
        limit = self.get_limit(pk)
        if 'calories' not in request.data:
            calories = get_calories(request.data['text']) # calls the nutrionix api
            request.data['calories'] = calories
        
        try:
            data = self.validate_and_save(request, limit)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = { 'error': str(e)}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        
    
    '''
    A get request for getting all calory instances for a given limit
    '''
    def get(self, request, pk):
        limit = self.get_limit(pk)
        calories = Calories.objects.filter(calory_limit=pk).all()
        serializer = CalorySerializer(calories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

'''
A get request for retrieving a given calory data
'''
class CaloryDetailsView(RetrieveAPIView):
    permission_classes = [IsOwnerOrReadOnly | ManagerEditDeletePermission]
    queryset = Calories.objects.all()
    serializer_class = CalorySerializer


'''
A get request for getting the amount of calories taken today
'''   
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

class EditDeleteCaloryView(APIView):
    permission_classes = [ IsOwnerOrReadOnly | ManagerEditDeletePermission | IsAdminUser ]
    '''
    Getting an instance of the calory limit model
    '''
    def get_calory_limit(self, pk):
        try:
            return CaloryLimit.objects.get(id=pk)
        except CaloryLimit.DoesNotExist:
            raise Http404
    

    '''
    Getting serialized data from the calory limit model
    '''
    def get_limit_serialized_data(self, pk):
        try:
            _limit = CaloryLimit.objects.get(id=int(pk))
            serializer = CaloryLimitSerializer(_limit)
            return serializer.data
        except CaloryLimit.DoesNotExist:
            raise Http404

    '''
    Getting an instance of the calory model
    ''' 
    def get_calory(self, pk):
        try:
            return Calories.objects.get(id=pk)
        except Calories.DoesNotExist:
            raise Http404

    '''
    Getting serialized data from the calory model
    ''' 
    def get_calory_serialized_data(self, pk):
        try:
            calory = Calories.objects.get(id=pk)
            serializer = CalorySerializer(calory)
            return serializer.data
        except Calories.DoesNotExist:
            raise Http404
    
    
    '''
    Removes the old calory amount from the calory limit instance anytime there is an update or delete
    '''
    def remove_old_calory_amount(self, calory):
        calory_limit = self.get_limit_serialized_data(calory['calory_limit'])
        calory_limit['present_calory_amount'] -= calory['calories']
        if calory_limit['present_calory_amount'] >= calory_limit['calory_limit']:
            calory_limit['exceeded_maximum'] = True
        else:
            calory_limit['exceeded_maximum'] = False
        return calory_limit

    '''
    Adds the new calory amount to the calory limit instance anytime there is an update
    '''
    def add_new_calory_amount(self, calory, calory_amount):
        calory_limit = self.get_limit_serialized_data(calory['calory_limit'])
        calory_limit['present_calory_amount'] += calory_amount
        if calory_limit['present_calory_amount'] >= calory_limit['calory_limit']:
            calory_limit['exceeded_maximum'] = True
        else:
            calory_limit['exceeded_maximum'] = False
        return calory_limit

    '''
    Updating a calory resource
    '''
    def put(self, request, pk):
        calory_ = self.get_calory(pk)
        calory = self.get_calory_serialized_data(pk)
        limit = self.get_calory_limit(calory['calory_limit'])
        try:
            limit_data = self.remove_old_calory_amount(calory)
            serializer = CaloryLimitSerializer(limit, data=limit_data) 
            if serializer.is_valid():
                serializer.save()
                # return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = {'error': str(e)}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        serializer = CalorySerializer(calory_, data=request.data)      
        if serializer.is_valid():
            try:
                limit_data = self.add_new_calory_amount(calory, request.data['calories'])
                limit_serializer = CaloryLimitSerializer(limit, data=limit_data)  
                if limit_serializer.is_valid():
                    limit_serializer.save()
                #     return Response(limit_serializer.data, status=status.HTTP_200_OK)
                # else:
                #     return Response(limit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                error_message = {'error': 'The error is here'}
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    '''
    Deleting a calory resource
    '''
    def delete(self, request, pk):
        calory = self.get_calory_serialized_data(pk)
        calory_ = self.get_calory(pk)
        limit = self.get_calory_limit(calory['calory_limit'])
        try:
            limit_data = self.remove_old_calory_amount(calory)
            serializer = CaloryLimitSerializer(limit, data=limit_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = {'error': str(e)}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        
        # delete calory
        calory_.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

