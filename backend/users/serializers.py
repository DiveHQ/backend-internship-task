from rest_framework.serializers import ModelSerializer

from .models import User


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
        user = User(
            email=validated_data["email"],
            name=validated_data["name"],
            username=validated_data["email"],
        )
        # identify password field to be set as hashed password
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        # identify password field to be set as hashed password
        instance.set_password(
            validated_data.get("password", instance.password)
        )
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("email", instance.username)
        instance.save()
        return instance
