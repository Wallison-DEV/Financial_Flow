from .models import AccountModel, CategoryModel, TransactionModel, TransferModel
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'

class TransactionSerlializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferModel
        fields = '__all__'