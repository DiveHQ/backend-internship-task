from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Calories


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    groups = serializers.SlugRelatedField(
        many=True, queryset=Group.objects.all(), slug_field="name"
    )

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.set(groups)
        return user

    class Meta:
        model = User
        fields = ("username", "password", "groups", "max_calories")


class CaloriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calories
        fields = ("id", "user", "date", "time", "text", "calories", "is_below_expected")
        read_only_fields = ("user", "calories", "is_below_expected")
