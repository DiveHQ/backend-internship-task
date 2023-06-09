from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Calories


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "password")


class CaloriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calories
        fields = ("id", "user", "date", "time", "text", "calories", "is_below_expected")
        read_only_fields = ("user", "calories", "is_below_expected")
