from rest_framework import serializers
from .models import User
from calori.models import Calo

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','daily_Cola')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'], 
                                        password=validated_data['password'],daily_Cola=validated_data['daily_Cola'])

        return user
    
class CaloSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Calo
        fields = ['id','name','quantity','calories','created_at','updated_at']