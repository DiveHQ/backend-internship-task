from django.shortcuts import render
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView

from .models import User
from app.permissions import UserEditDeletePermission


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class UserDetailsView(UpdateAPIView):
    permission_classes = [UserEditDeletePermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
