from rest_framework import serializers

from .models import UserModel, ProfileModel

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model= UserModel
        fields= ['id', 'email', 'username', 'password']
        extra_kwargs= {'password': {'write_only': True}}

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)
    
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta: 
        model= ProfileModel
        fields= '__all__'