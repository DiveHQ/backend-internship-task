from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Entry
from .serializers import EntrySerializer
from rest_framework.permissions import BasePermission

from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from . import calories_calculator

User = get_user_model()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.role == "admin"
        else:
            return False


# @api_view(["GET"])
# @permission_classes([IsAdmin])
# def all_entries(request):
#     entries = Entry.objects.all()
#     entry_serializer = EntrySerializer(entries, many=True)

#     users = User.objects.all()
#     user_serializer = UserSerializer(users, many=True)

#     data = {"All Entries": entry_serializer.data, "All Users": user_serializer.data}


#     return Response(data)


@api_view(["GET"])
@permission_classes([IsAdmin])
def all_entries(request):
    entries = Entry.objects.all()
    serializer = EntrySerializer(entries, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdmin])
def all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = request.data

        # Update the user's account details
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.expected_calories = data.get("expected_calories", user.expected_calories)
        password = data.get("password")
        if password:
            user.set_password(password)

        user.save()

        return Response("Account details updated successfully")


import requests


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def entry_list(request):
    if request.method == "GET":
        entries = Entry.objects.filter(user=request.user)
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            # Fetch calorie information using the calories_calculator.get_calories function
            food_name = serializer.validated_data.get("text")
            calories = serializer.validated_data.get("calories")
            if not calories:
                calories = calories_calculator.get_calories(food_name)

            if calories is not None:
                # Assign the fetched calorie information to the serializer data
                serializer.validated_data["calories"] = calories

            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def entry_detail(request, pk):
    try:
        entry = Entry.objects.get(pk=pk)
    except Entry.DoesNotExist:
        return Response("No Records found", status=404)

    # Check if the user is the owner of the entry or has the role of "Admin"
    if request.user == entry.user or request.user.role == "admin":
        if request.method == "GET":
            serializer = EntrySerializer(entry)
            return Response(serializer.data)

        elif request.method == "PUT":
            serializer = EntrySerializer(entry, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        elif request.method == "DELETE":
            entry.delete()
            return Response(status=204)
    else:
        return Response("Unauthorized", status=403)
