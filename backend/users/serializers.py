from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from rest_framework.exceptions import APIException, status
from rest_framework.serializers import ModelSerializer

from .models import User, UserSettings


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "name": {"required": True},
        }

        fields = ["email", "name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create(**validated_data)

        # identify password field to be set as hashed password
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, password):
        # validate password using django's password validation
        django_validate_password(password, self.context["request"].user)
        return password

    def update(self, instance, validated_data):
        # identify password field to be set as hashed password
        password = validated_data.pop("password", instance.password)
        instance.set_password(password)
        return super().update(instance, validated_data)


class UserSettingsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "expected_daily_calories": {"required": True},
        }

    def create(self, validated_data):
        user = validated_data["user"]
        settings, created = UserSettings.objects.get_or_create(
            user=user, defaults=validated_data
        )
        if not created:
            raise APIException(
                "User settings already exist.",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return settings
