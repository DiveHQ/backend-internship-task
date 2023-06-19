from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Entry
from .serializers import EntrySerializer

# from rest_framework.permissions import BasePermission

from django.contrib.auth import get_user_model

# from accounts.serializers import UserSerializer
from . import calories_calculator
from rest_framework.pagination import PageNumberPagination

User = get_user_model()


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def entry_list(request):
    if request.method == "GET":
        date = request.GET.get("date")
        query = request.GET.get("query")

        entries = Entry.objects.filter(user=request.user)

        # Filter entries based on query parameters
        if query:
            entries = entries.filter(text__icontains=query)
        # Filter entries by date if provided
        if date:
            entries = entries.filter(date=date)

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Set the number of entries per page
        paginated_entries = paginator.paginate_queryset(entries, request)

        serializer = EntrySerializer(paginated_entries, many=True)
        return paginator.get_paginated_response(serializer.data)
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
