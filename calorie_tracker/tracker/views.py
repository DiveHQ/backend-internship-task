from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Entry
from .serializers import EntrySerializer
from rest_framework.permissions import BasePermission

from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from . import calories_calculator
from rest_framework.pagination import PageNumberPagination

User = get_user_model()


# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         if request.user:
#             return request.user.role == "admin"
#         else:
#             return False


# class IsUserManager(BasePermission):
#     def has_permission(self, request, view):
#         if request.user:
#             # return request.user.role == "user_manager"
#             return request.user.role in ["admin", "user_manager"]
#         else:
#             return False


# @api_view(["GET"])
# @permission_classes([IsAdmin])
# def all_entries(request):
#     entries = Entry.objects.all()

#     # Filter entries based on query parameters
#     query = request.GET.get("query")
#     if query:
#         entries = entries.filter(text__icontains=query)

#     # Apply pagination
#     paginator = PageNumberPagination()
#     paginator.page_size = 5  # Number of entries per page
#     paginated_entries = paginator.paginate_queryset(entries, request)

#     serializer = EntrySerializer(paginated_entries, many=True)
#     return paginator.get_paginated_response(serializer.data)

#     # serializer = EntrySerializer(entries, many=True)
#     # return Response(serializer.data)


# @api_view(["GET"])
# @permission_classes([IsUserManager])
# def all_users(request):
#     users = User.objects.all()

#     # Filter entries based on query parameters
#     query = request.GET.get("query")
#     if query:
#         users = users.filter(username__icontains=query)

#     # Apply pagination
#     paginator = PageNumberPagination()
#     paginator.page_size = 5  # Number of entries per page
#     paginated_users = paginator.paginate_queryset(users, request)

#     serializer = UserSerializer(paginated_users, many=True)
#     return paginator.get_paginated_response(serializer.data)

#     # serializer = UserSerializer(users, many=True)
#     # return Response(serializer.data)


# @api_view(["GET", "PUT"])
# @permission_classes([IsAuthenticated])
# def profile(request):
#     user = request.user

#     if request.method == "GET":
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         data = request.data

#         # Update the user's account details
#         user.username = data.get("username", user.username)
#         user.email = data.get("email", user.email)
#         user.expected_calories = data.get("expected_calories", user.expected_calories)
#         password = data.get("password")
#         if password:
#             user.set_password(password)

#         user.save()

#         return Response("Account details updated successfully")


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
