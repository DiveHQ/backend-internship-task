from rest_framework import generics, permissions,status
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.models import User
from .serializer import UserSerializer, RegisterSerializer , CaloSerializer
from .models import Calo
from .pagenation import CustomPagination
import requests
import json
"""from .env import SECRET_KEY"""


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

#login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



#CRUD Section for Calories

class  CaloView(APIView):
  permission_classes = [permissions.AllowAny]
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
    Calor = Calo.objects.all()
    page = self.paginate_queryset(Calor)
    if page is not None:
            serializer = self.get_paginated_response(CaloSerializer(page,
 many=True).data)
    else:
            serializer = CaloSerializer(Calor, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  

  def post(self, request, *args, **kwargs):
    calories =  request.data.get('calories')
    if not calories:
       query = request.data.get('name')
       api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
       response = requests.get(api_url, headers={'X-Api-Key': "QQ8RM7o93r8tFonRPHaRpw==YyWb0znekP61Q8Ua"}).json()
       cal=  response[0]['calories']
       calories = int(cal)
    
    data = {
        'name': request.data.get('name'), 
        'quantity': request.data.get('quantity'),
        'calories': calories
    }

    serializer = CaloSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  def delete(self, request, id, *args, **kwargs):
      if Calo.objects.filter(id=id).exists():
        project = Calo.objects.get(id=id)
        project.delete()
        return Response({"response":"Calo Deleted"}, status=status.HTTP_200_OK)
      else:
          return Response(
              {"res": "Calo Doesn't Exists"},
              status=status.HTTP_400_BAD_REQUEST
          )

  def patch(self, request, id, *args, **kwargs):
    if Calo.objects.filter(id=id).exists():
      project = Calo.objects.get(id=id)
      data = {
      'title': request.data.get('title'), 
      'description': request.data.get('description'), 
      }
      serializer = CaloSerializer(instance = project, data=data, partial = True)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
                {"res": "Calo Doesn't Exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )


#crud users

class UserManger(APIView):
  permissions_classes = (permissions.AllowAny)
  def get(self,requst,*args,**kwargs):
     user = User.objects.all()