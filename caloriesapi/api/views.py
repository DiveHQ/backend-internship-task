from datetime import date
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import User
from django.contrib.auth import login, authenticate
from .models import Calories
from .serializers import CaloriesSerializer, UserSerializer, GroupUpdateSerializer


# Permission Classes
class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="User Manager").exists()
        )


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuer


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, _, obj):
        return request.user.is_superuser or obj.user == request.user


# Views
@api_view(["POST"])
def create_account(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User Account created succesfully"}, status=201)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(["POST"])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        session_cookie = request.session.session_key
        return Response(
            {"message": "Login Successful", "session_cookie": session_cookie},
            status=200,
        )
    return Response({"message": "Invalid credentials"}, status=401)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminOrManager])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=200)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def update_user_groups(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    serializer = GroupUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User groups updated successfully"}, status=200)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_calorie_entry(request):
    serializer = CaloriesSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        entry = serializer.save(user=user)
        entry.get_calories()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def get_calorie_entry(request, pk):
    try:
        entry = Calories.objects.get(pk=pk)
    except Calories.DoesNotExist:
        return Response({"message": "Calorie entry not found."}, status=404)
    serializer = CaloriesSerializer(entry)
    return Response(serializer.data, status=200)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def update_calorie_entry(request, pk):
    try:
        entry = Calories.objects.get(pk=pk)
    except Calories.DoesNotExist:
        return Response({"message": "Calorie entry not found."}, status=404)
    serializer = CaloriesSerializer(entry, data=request.data, partial=True)
    if serializer.is_valid():
        entry = serializer.save()
        entry.get_calories()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def delete_calorie_entry(request, pk):
    try:
        entry = Calories.objects.get(pk=pk)
    except Calories.DoesNotExist:
        return Response({"message": "Calorie entry not found."}, status=404)
    entry.delete()
    return Response({"message": "Calorie entry deleted successfully."}, status=204)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_calorie_entries(request):
    entry = Calories.objects.filter(user=request.user)
    serializer = CaloriesSerializer(entry, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_calorie_entries_by_date(request):
    date_param = request.query_params.get("date", None)
    if date_param:
        try:
            entries = Calories.objects.filter(
                user=request.user, date=date.fromisoformat(date_param)
            )
            serializer = CaloriesSerializer(entries, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"message": "Invalid date format."}, status=400)
    return Response({"message": "Date parameter is required."}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_calorie_entries_by_status(request):
    status = request.query_params.get("status", None)
    if status:
        entries = Calories.objects.filter(
            user=request.user, is_below_expected=(status == "below")
        )
        serializer = CaloriesSerializer(entries, many=True)
        return Response(serializer.data, status=200)
    return Response({"message": "Status parameter is required"}, status=400)