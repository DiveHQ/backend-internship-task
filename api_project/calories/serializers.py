from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import serializers

from .models import Calories
from .utils import get_calories_from_meal


class CaloriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calories
        fields = ["id", "user", "meal", "calories", "note", "extra", "created_at"]
        extra_kwargs = {"extra": {"read_only": True}}

    def validate(self, data):
        validated_data = super().validate(data)
        meal = validated_data.get("meal")
        calories = validated_data.get("calories")
        if not calories:
            # fetch calories from api
            res = get_calories_from_meal(meal)
            # add calories to
            validated_data["calories"] = res
        return validated_data

    def get_total_calories_for_today(self, user):
        today = timezone.now().date()
        # Get user's calories for today
        total = Calories.objects.filter(user=user, created_at__date=today).aggregate(
            total=Coalesce(Sum("calories"), 0)
        )
        return total.get("total", 0)

    def create(self, validated_data):
        user = validated_data.get("user")
        new_calories = validated_data.get("calories")

        calories_for_today = self.get_total_calories_for_today(user)
        total_for_today = calories_for_today + new_calories

        if user.calories_per_day > total_for_today:
            return Calories.objects.create(**validated_data, extra=True)
        return super().create(validated_data)
