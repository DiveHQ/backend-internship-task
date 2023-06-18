from rest_framework import generics, permissions,status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth import login
from .models import User
from django.contrib.auth.models import Group
from .serializer import UserSerializer, RegisterSerializer
from django.contrib.auth.decorators import permission_required
from .pagenation import CustomPagination


"""from .env import SECRET_KEY"""


"""Register API"""

class RegisterAPI(generics.GenericAPIView):
    permission_classes = [AllowAny] 
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
          """try:"""
         
          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = serializer.save()
          user = UserSerializer(user, context=self.get_serializer_context()).data
          
          gp =User.objects.filter(username=request.data.get("username")).get()
          group = Group.objects.get_or_create(name='Client')
          group =Group.objects.get(name='Client')
          gp.groups.add(group)
          
         
          return Response({"user":user})
          """except:
        return Response("Invalid Details! ")"""
        
          

"""login API"""

class LoginAPI(KnoxLoginView):
    permission_classes = [AllowAny] 

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        
        return super(LoginAPI, self).post(request,format=None)

"""crud users"""
class UserManger(APIView):  
  
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
          if user2.has_perm('authen.add_user'):
          
              user = User.objects.all().order_by('id')
              page = self.paginate_queryset(user)
              if page is not None:
                      serializer = self.get_paginated_response(UserSerializer(page,many=True).data)
              else:
                serializer = UserSerializer(user, many=True)
              return Response(serializer.data, status=status.HTTP_200_OK)
                
          else:
            return Response({
                  "res":"Unauthorized"
                })   
  def post(self,request,*args,**kwargs): 
            user = request.user     
            if user.has_perm("authen.view_user") :
             
                data = {
                  'username': request.data.get('username'), 
                  'email': request.data.get('email'),
                  'password': request.data.get('password'),
                  'daily_calo': request.data.get('daily_calo')
                  }

                serializer = RegisterSerializer(data=data)
                if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
              
            else:
              return Response({
                  "res":"Unauthorized"
                })  
          
  def delete(self, request, id, *args, **kwargs):
        user = request.user     
        if  user.has_perm('authen.delete_user'):
                if User.objects.filter(id=id).exists():
                  project = User.objects.get(id=id)
                  project.delete()
                  return Response({"response":"User Deleted"}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"res": "User Doesn't Exists"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
        else:
            return Response({
                  "res":"Unauthorized"
                })              
  def patch(self, request, id, *args, **kwargs):
        user = request.user     
        if user.has_perm('authen.change_user'):
                if User.objects.filter(id=id).exists():
                  project = User.objects.filter(id=id).get()
                  serializer = UserSerializer(instance = project, data=request.data, partial = True)
                  if serializer.is_valid():
                      serializer.save()
                      return Response(serializer.data, status=status.HTTP_200_OK)
                  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(
                            {"res": "User Doesn't Exists"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
        else:
              return Response({
                  "res":"Unauthorized"
                })  