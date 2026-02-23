from rest_framework import serializers

from .models import UserModel, ProfileModel

class UserSerializer(serializers.ModelSerializer):
    monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    currency_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'username', 'password', 'monthly_income', 'currency_id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        income = validated_data.pop('monthly_income')
        currency_id = validated_data.pop('currency_id')

        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email'].split('@')[0]
            
        user = UserModel.objects.create_user(**validated_data)
        
        from currencies.models import CurrencyModel
        currency = CurrencyModel.objects.get(id=currency_id)

        from .services import setup_initial_user_data
        setup_initial_user_data(user, income, currency)

        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta: 
        model= ProfileModel
        fields= '__all__'