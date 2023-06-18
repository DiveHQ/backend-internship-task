from rest_framework import  permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from authen.serializer import  CaloSerializer
from .models import Calo
from authen.pagenation import CustomPagination
import requests
from authen.models import User
from rest_framework.permissions import IsAuthenticated
import json
# Create your views here.
#CRUD Section for Calories
import os

class  CaloView(APIView):
   
  permission_classes = [IsAuthenticated]
  pagination_class = CustomPagination
  

  @property
  def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator
  def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                   self.request, view=self)
  def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
      
  
 
  def get(self,request,*args,**kwargs):
    user2 = request.user 
    user2 =User.objects.filter(id=user2.id).get()    
    if user2.has_perm('calori.view_calo'):
          user=request.user.id
          """
          apply filters with for only userID's contain and 
          think there is no need to apply additional filter features
          """
          Calor = Calo.objects.filter(user=user).all().order_by("id")
          page = self.paginate_queryset(Calor)
          if page is not None:
                  serializer = self.get_paginated_response(CaloSerializer(page,
      many=True).data)
          else:
                  serializer = CaloSerializer(Calor, many=True)
          return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response({
                  "res":"Unauthorized"
                },status=status.HTTP_401_UNAUTHORIZED)   
      
  def post(self, request, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
          with open(os.path.join(BASE_DIR, 'secret.json')) as handle:
            SECRETS = json.load(handle)
        except IOError:
          SECRETS = {}
      
        key=SECRETS['API_KEY']
        user2 = request.user 
        user2 =User.objects.filter(id=user2.id).get()    
        if user2.has_perm('calori.add_calo'):
          calories =  request.data.get('calories')
          if not calories:
            try:
              query = request.data.get('name')
              api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
              response = requests.get(api_url, headers={'X-Api-Key':key }).json()
              cal=  response[0]['calories']
              calories = int(cal)
            except:
              return{
                "msg":"could not automate Calories for{query}"
              }
          
          data = {
              'name': request.data.get('name'), 
              'quantity': request.data.get('quantity'),
              'calories': calories,
              'limit_reach':request.data.get('limit_reach')
                ,'user': request.user.id
          }
          
          serializer = CaloSerializer(data=data)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
          return Response({
                  "res":"Unauthorized"
                },status=status.HTTP_401_UNAUTHORIZED)   
          
  def delete(self, request, id, *args, **kwargs):
      user2 = request.user 
      user2 =User.objects.filter(id=user2.id).get()    
      if user2.has_perm('calori.delete_calo'):
            user=request.user.id
            if Calo.objects.filter(user=user).filter(id=id).exists():
              project = Calo.objects.filter(user=user).get(id=id)
              project.delete()
              return Response({"msg":"Calo Deleted"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"msg": "Calo Doesn't Exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
      else:
        return Response({
                  "res":"Unauthorized"
                },status=status.HTTP_401_UNAUTHORIZED)   
  
  def patch(self, request, id, *args, **kwargs):
      user2 = request.user 
      user2 =User.objects.filter(id=user2.id).get()    
      if user2.has_perm('calori.change_calo'):
          user=request.user.id
          if Calo.objects.filter(user=user).filter(id=id).exists():
                  
                  """
                  the assumption here is that when a user request to for update
                  they can decide to update one or all
                  """
                  calor = Calo.objects.filter(id=id).get()
                  serializer = CaloSerializer(instance=calor,data=request.data,partial=True)
                  if serializer.is_valid():
                      serializer.save()
                      return Response(serializer.data, status=status.HTTP_200_OK)
                  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          else:    
            return Response(
                    {"res": "Calo Doesn't Exists"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
      else:
        return Response({
                  "res":"Unauthorized Access!"
                },status=status.HTTP_401_UNAUTHORIZED) 