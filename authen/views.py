from rest_framework import generics, permissions,status,Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from django.shortcuts import render
from django.contrib.auth import login
from .serializer import UserSerializer, RegisterSerializer , CaloSerializer
from .models import Calo

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

  def get(self,request,*args,**kwargs):
    projects = Calo.objects.all()
    serializer = CaloSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def post(self, request, *args, **kwargs):
    data = {
        'name': request.data.get('name'), 
        'quantity': request.data.get('quantity'),
        'calories': request.data.get('calories')
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


