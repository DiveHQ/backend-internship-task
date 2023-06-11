from rest_framework import serializers
from .models import CaloryLimit

class CaloryLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaloryLimit
        fields = '__all__'