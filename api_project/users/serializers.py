from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """
    serializer for signing up a new user
    """

    password = serializers.CharField(min_length=6, write_only=True)
    password2 = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "name", "password", "password2"]

    # Check if passwords match
    def validate_password2(self, password2: str):
        if self.initial_data.get("password") != password2:
            raise serializers.ValidationError("passwords do not match")
        return password2

    def create(self, validated_data: dict):
        # Remove second password field
        _ = validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


class SignupResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "name", "email", "role", "token")

    @swagger_serializer_method(
        serializer_or_field=serializers.JSONField(),
    )
    def get_token(self, user: User):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "role", "id"]
        extra_kwargs = {"role": {"read_only": True}}
