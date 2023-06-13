from core.constants import User
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from rest_framework import serializers

from .models import UserSettings


class PasswordSerializer(serializers.ModelSerializer):
    """Password serializer."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = ["password"]

    def update(self, user, validated_data):
        """Update user with an encrypted password and return the updated user."""
        password = validated_data.pop("password", None)

        user = super().update(user, validated_data)
        self.set_user_password(password, user)

        return user

    def validate_password(self, password):
        """Validate the password using Django's password validators."""
        django_validate_password(password, self.context["request"].user)
        return password

    def set_user_password(self, password, user: User):
        """Set the encrypted password for the user."""
        if password:
            user.set_password(password)
            user.save()


class UserSerializer(PasswordSerializer):
    """User model serializer. Inherits from PasswordSerializer."""

    class Meta(PasswordSerializer.Meta):
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ] + PasswordSerializer.Meta.fields

    def create(self, validated_data):
        """Create and return a user with an encrypted password."""
        password = validated_data.pop("password", None)

        user = User.objects.create(**validated_data)
        self.set_user_password(password, user)

        return user


class UserSettingsSerializer(serializers.ModelSerializer):
    """UserSettings model serializer."""

    class Meta:
        model = UserSettings
        fields = [
            "id",
            "user",
            "expected_daily_calories",
        ]
        read_only_fields = [
            "id",
            "user",
        ]

    def create(self, validated_data):
        """Create user settings or raise an error if they already exist."""
        user = validated_data["user"]
        settings, created = UserSettings.objects.get_or_create(user=user, defaults=validated_data)

        if not created:
            raise serializers.ValidationError(
                {"detail": "Settings already exist for the request user."}
            )

        return settings
