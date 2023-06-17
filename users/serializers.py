from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'password', 'phone_number', 'expected_calories', 'is_admin', 'is_user_manager']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_admin': {'read_only': True},
            'is_user_manager': {'read_only': True}
        }

    def to_representation(self, instance):
        """
        Customize the serialized representation of the User model.
        Exclude 'is_admin' and 'is_user_manager' fields for non-admin/non-user-manager users.
        """
        # Get the current user making the request
        user = self.context['request'].user

        # If the user is not an admin or user manager, exclude some fields
        if not user.is_admin and not user.is_user_manager:
            self.fields.pop('is_admin', None)
            self.fields.pop('is_user_manager', None)

        return super().to_representation(instance)

    def create(self, validated_data):
        """
        Create a new user instance and hash the password before saving.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
