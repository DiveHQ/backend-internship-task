from rest_framework import serializers
from .models import Entry
from django.db import models

class EntrySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Entry model.

    This serializer is used to convert Entry model instances to JSON and vice versa.
    It also includes custom validation and logic for calculating the calorie goal met.

    Attributes:
        model (class): The model associated with the serializer.
        fields (tuple/list): The fields to include in the serialized representation.
        read_only_fields (tuple/list): The fields that should be read-only when deserializing.

    Methods:
        create(validated_data): Creates a new Entry instance with the given validated data.
        update(instance, validated_data): Updates an existing Entry instance with the given validated data.
        calculate_calorie_goal_met(entry, expected_calories_per_day=None): Calculates and updates the calorie goal met field for the given Entry instance.

    """

    class Meta:
        model = Entry
        fields = '__all__'
        read_only_fields = ('meets_calorie_expectation',)

    def create(self, validated_data):
        """
        Create and return a new Entry instance with the given validated data.

        Args:
            validated_data (dict): The validated data for creating the Entry instance.

        Returns:
            Entry: The created Entry instance.

        Raises:
            serializers.ValidationError: If the expected calories per day is not set for the user.

        """

        user = validated_data.get('user')
        expected_calories = user.expected_calories

        if expected_calories is None:
            raise serializers.ValidationError("Expected calories per day is not set for the user.")

        entry = super().create(validated_data)
        self.calculate_calorie_goal_met(entry, expected_calories)
        return entry

    def update(self, instance, validated_data):
        """
        Update and return an existing Entry instance with the given validated data.

        Args:
            instance (Entry): The existing Entry instance to update.
            validated_data (dict): The validated data for updating the Entry instance.

        Returns:
            Entry: The updated Entry instance.

        Raises:
            serializers.ValidationError: If the expected calories per day is not set for the user.

        """

        user = validated_data.get('user')
        expected_calories = user.expected_calories

        if expected_calories is None:
            raise serializers.ValidationError("Expected calories per day is not set for the user.")

        entry = super().update(instance, validated_data)
        self.calculate_calorie_goal_met(entry, expected_calories)
        return entry

    def calculate_calorie_goal_met(self, entry, expected_calories_per_day=None):
        """
        Calculate and update the calorie goal met field for the given Entry instance.

        Args:
            entry (Entry): The Entry instance for which to calculate the calorie goal met.
            expected_calories_per_day (int, optional): The expected calories per day for the user.

        Returns:
            None

        """

        user = entry.user
        total_calories_for_day = Entry.objects.filter(user=user, date=entry.date).aggregate(total_calories=models.Sum('calories'))['total_calories']

        if total_calories_for_day is not None and expected_calories_per_day is not None:
            entry.meets_calorie_expectation = total_calories_for_day < expected_calories_per_day
            entry.save()
