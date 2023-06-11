from rest_framework import serializers
from .models import Calories, CaloryLimit

class CalorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Calories
        fields = '__all__'

    def validate_calories(self, attrs):
        if attrs < 0:
            raise serializers.ValidationError('Calories cannot be a negative number')
        return attrs


        
class CaloryLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaloryLimit
        fields = '__all__'