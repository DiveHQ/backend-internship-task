from rest_framework import serializers
from .models import CaloryLimit

class CaloryLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaloryLimit
        fields = '__all__'
    

    def validate_calory_limit(self, calory_limit):
        if calory_limit <= 0:
            raise serializers.ValidationError('Calory Limit cannot be negative')
        return calory_limit