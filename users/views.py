from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .authentication import TokenAuthentication
from .permissions import IsAdminOrUserManager
from .models import User


class LoginView(APIView):
    """
    View for user login.

    POST:
    Perform user login by authenticating the user with provided email and password.
    Returns a token if the login is successful, or an error message if the credentials are invalid.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Perform user login.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    View for user logout.

    POST:
    Perform user logout by deleting the authentication token associated with the user.
    Returns a success message upon successful logout.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        """
        Perform user logout.
        """
        request.user.auth_token.delete()
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    """
    View for user registration.

    POST:
    Register a new user by creating a new user instance with the provided data.
    Returns a token for the registered user upon successful registration, or validation errors if the data is invalid.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Register a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    """
    View for deleting a user.

    DELETE:
    Delete a user based on the provided user ID. Only administrators or user managers can delete users.
    If no user ID is provided, the currently authenticated user will be deleted.
    Returns a success message upon successful deletion or an error message if the user is not found or unauthorized.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        """
        Delete a user.
        """
        if request.user.is_admin or request.user.is_user_manager:
            user_id = request.data.get('id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    user.delete()
                    return Response({'detail': 'User deleted successfully'}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        request.user.delete()
        return Response({'detail': 'User deleted successfully'}, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    """
    View for updating a user.

    PATCH:
    Update a user based on the provided user ID and data. Only administrators or user managers can update users.
    If no user ID is provided, the currently authenticated user will be updated.
    Returns the updated user data upon successful update or validation errors if the data is invalid.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request):
        """
        Update a user.
        """
        if request.user.is_admin or request.user.is_user_manager:
            user_id = request.data.get('id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
                    if serializer.is_valid():
                        user = serializer.save()
                        updated_serializer = UserSerializer(user, context={'request': request})
                        return Response(updated_serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            updated_serializer = UserSerializer(user, context={'request': request})
            return Response(updated_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersView(APIView):
    """
    View for listing users.

    GET:
    Retrieve a list of all users. Only administrators or user managers can access this view.
    Returns a list of serialized user data upon successful retrieval.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrUserManager]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        Retrieve a list of all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    View for retrieving a user.

    GET:
    Retrieve a user based on the provided user ID. Administrators or user managers can retrieve all users.
    Users can only retrieve their own data.
    If no user ID is provided, the currently authenticated user will be retrieved.
    Returns the serialized user data upon successful retrieval or an error message if the user is not found or unauthorized.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        Retrieve a user.
        """
        if request.user.is_admin or request.user.is_user_manager:
            user_id = request.data.get('id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    serializer = UserSerializer(user, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
