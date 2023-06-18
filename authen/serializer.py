from rest_framework import serializers
from .models import User
from calori.models import Calo
from django.contrib.auth.hashers import make_password
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(
        min_length=6, write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','daily_calo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
    
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], 
                                        password=validated_data['password'],daily_calo=validated_data['daily_calo'])

        return user
    
class CaloSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Calo
        fields = ['id','name','quantity','calories','created_at','updated_at','user',"limt_reach"]
       
        
        def create(self, validated_data):
            user=User.objects.get(user=self.user)
            calories = Calo.objects.create(name=validated_data['name'], quantity=validated_data['quantity'], 
                                        calories=validated_data['calories'],created_at=validated_data['created_at'],
                                        updated_at=validated_data['updated_at'],user=validated_data[user],limt_reach=validated_data['limt_reach'])
            
            return calories