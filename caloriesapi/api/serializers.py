from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import Calories, User
from caloriesapi.settings import AUTH_USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ("id", "username", "password", "max_calories")


class CaloriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calories
        fields = ("id", "user", "date", "time", "text", "calories", "is_below_expected")
        read_only_fields = ("user", "calories", "is_below_expected")


class GroupUpdateSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        slug_field="name",
    )

    class Meta:
        model = User
        fields = ("groups",)
