from rest_framework import  permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from authen.serializer import  CaloSerializer
from .models import Calo
from authen.pagenation import CustomPagination
from django_filters import rest_framework as filters
import requests
from  django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.decorators import login_required, permission_required
from authen.filters import calo_Filter
from authen.models import User
# Create your views here.
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
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name', 'id')
    
    
    #trying to implement filters
    
    """"Calor = calo_Filter(request.GET, queryset= Calo.objects.all())"""
    """      
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'id']
    """
    
    """
      if name:
        Calor = Calor(name__icontains=name)
    """
    
     
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
        'calories': calories,
        'limit_reach':request.data.get('limit_reach')
          ,'user': request.user.id
    }
    
    serializer = CaloSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  @login_required
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
  @login_required
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