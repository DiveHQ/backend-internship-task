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
        fields = ('id', 'username', 'email', 'password','daily_calo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'], 
                                        password=validated_data['password'],daily_calo=validated_data['daily_calo'])

        return user
    
class CaloSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Calo
        fields = ['id','name','quantity','calories','created_at','updated_at','user']
        
        """def create(self, validated_data):
            user=User.objects.get(user=self.user)
            calories = Calo.objects.create(name=validated_data['name'], quantity=validated_data['quantity'], 
                                        calories=validated_data['calories'],created_at=validated_data['created_at'],
                                        updated_at=validated_data['updated_at'],user=validated_data[user])
            
            return calories"""