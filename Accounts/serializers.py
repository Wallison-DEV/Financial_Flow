from .models import AccountModel, CategoryModel, TransactionModel, TransferModel
from rest_framework import serializers
from django.db import IntegrityError

class AccountSerializer(serializers.ModelSerializer):
    

    def  create(self, validated_data):
        try:
            return AccountModel.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Já existe uma conta com esse nome.")
    

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
        fields = "__all__"
        read_only_fields = (
            "converted_amount",
            "destination_currency",
            "created_at",
            "updated_at",
        )