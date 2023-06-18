from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tracker.models import Entry
from tracker.serializers import EntrySerializer
from rest_framework.permissions import BasePermission

from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer

# from . import calories_calculator
from rest_framework.pagination import PageNumberPagination

User = get_user_model()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.role == "admin"
        else:
            return False


class IsUserManager(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            # return request.user.role == "user_manager"
            return request.user.role in ["admin", "user_manager"]
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

    # Filter entries based on query parameters
    query = request.GET.get("query")
    if query:
        entries = entries.filter(text__icontains=query)

    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Number of entries per page
    paginated_entries = paginator.paginate_queryset(entries, request)

    serializer = EntrySerializer(paginated_entries, many=True)
    return paginator.get_paginated_response(serializer.data)

    # serializer = EntrySerializer(entries, many=True)
    # return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsUserManager])
def all_users(request):
    users = User.objects.all()

    # Filter entries based on query parameters
    query = request.GET.get("query")
    if query:
        users = users.filter(username__icontains=query)

    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Number of entries per page
    paginated_users = paginator.paginate_queryset(users, request)

    serializer = UserSerializer(paginated_users, many=True)
    return paginator.get_paginated_response(serializer.data)

    # serializer = UserSerializer(users, many=True)
    # return Response(serializer.data)


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
