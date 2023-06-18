from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from users.authentication import TokenAuthentication
from users.models import User
from .models import Entry
from .permissions import (
    EntriesCreateObjectLevelPermission,
    EntriesObjectLevelPermission,
    IsAdmin
)
from .serializers import EntrySerializer


class CreateEntryView(APIView):
    """
    API view for creating a new entry.
    Requires authentication and permission to create entries.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, EntriesCreateObjectLevelPermission]

    def post(self, request):
        """
        Create a new entry.

        Request data:
        - user_id: The ID of the user creating the entry.

        Returns the serialized entry object if successful, or an error response if unsuccessful.
        """

        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['user'] = user_id
        data.pop('user_id')

        serializer = EntrySerializer(data=data)
        if serializer.is_valid():
            entry = serializer.save(user=user)
            updated_serializer = EntrySerializer(entry)
            return Response(updated_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEntryView(APIView):
    """
    API view for updating an existing entry.
    Requires authentication and permission to update entries.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, EntriesObjectLevelPermission]

    def patch(self, request):
        """
        Update an existing entry.

        Request data:
        - entry_id: The ID of the entry to update.
        (Include the fields you want to update in the request data.)

        Returns the serialized entry object if successful, or an error response if unsuccessful.
        """

        entry_id = request.data.get('entry_id')
        try:
            entry = Entry.objects.get(id=entry_id)
        except Entry.DoesNotExist:
            return Response({'detail': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EntrySerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=entry.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEntryView(APIView):
    """
    API view for deleting an existing entry.
    Requires authentication and permission to delete entries.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, EntriesObjectLevelPermission]

    def delete(self, request):
        """
        Delete an existing entry.

        Request data:
        - entry_id: The ID of the entry to delete.

        Returns a success response if deletion is successful, or an error response if unsuccessful.
        """

        entry_id = request.data.get('entry_id')
        try:
            entry = Entry.objects.get(id=entry_id)
        except Entry.DoesNotExist:
            return Response({'detail': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListEntriesView(APIView):
    """
    API view for listing all entries.
    Requires authentication and admin permission.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        """
        Get a list of all entries.

        Returns the serialized list of entry objects.
        """

        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EntryDetailView(APIView):
    """
    API view for retrieving details of a specific entry.
    Requires authentication and permission to access entries.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, EntriesObjectLevelPermission]

    def get(self, request):
        """
        Get the details of a specific entry.

        Request data:
        - entry_id: The ID of the entry to retrieve.

        Returns the serialized entry object if successful, or an error response if unsuccessful.
        """

        entry_id = request.data.get('entry_id')
        try:
            entry = Entry.objects.get(id=entry_id)
        except Entry.DoesNotExist:
            return Response({'detail': 'Entry not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EntrySerializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)
