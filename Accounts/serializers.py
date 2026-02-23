from .models import AccountModel, CategoryModel, RecurringTransactionModel, TransactionModel, TransferModel
from rest_framework import serializers
from django.db import IntegrityError

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def  create(self, validated_data):
        try:
            return AccountModel.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Já existe uma conta com esse nome.")
    

    class Meta:
        model = AccountModel
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CategoryModel
        fields = ['id', 'name', 'type', 'parent', 'icon', 'color', 'ordering', 'user', 'user_name'] 
        extra_kwargs = {'ordering': {'required': False, 'default': 0}}

    def validate_parent(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("A categoria pai deve pertencer a você.")
        return value

class TransactionSerlializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        read_only_fields = ['original_currency', 'converted_amount']
        fields = '__all__'

    def to_representation(self, instance):
        if isinstance(instance, dict):
            return super().to_representation(instance
                                             )
        repr = super().to_representation(instance)
        repr['user'] = instance.account.user.username
        repr['original_currency'] = instance.original_currency.name
        repr['category'] = instance.category.name
        repr['account'] = instance.account.name
        repr['original_amount'] = f"{instance.original_currency.symbol}{instance.original_amount}"
        repr['converted_amount'] = f"{instance.account.currency.symbol}{instance.converted_amount}"
        return repr

    def validate_account(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("Esta conta não pertence a você.")
        return value

    def validate_category(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("Esta categoria não pertence a você.")
        return value
    
    def validate(self, data):
        credit_card = data.get('credit_card')
        installments = data.get('installments', 1)
        category = data.get('category')
        tx_type = data.get('type')

        if category and tx_type and category.type != tx_type:
            raise serializers.ValidationError(
                {"type": "Tipo da transação deve corresponder ao tipo da categoria."}
            )

        if credit_card and installments < 1:
            raise serializers.ValidationError(
                {"installments": "Parcelamento inválido."}
            )

        return data
    
class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferModel
        fields = "__all__"
        read_only_fields = ("converted_amount", "destination_currency", "original_currency")

    def validate(self, data):
        user = self.context['request'].user
        if data['source_account'].user != user or data['destination_account'].user != user:
            raise serializers.ValidationError("Ambas as contas devem pertencer ao seu usuário.")
        return data

class RecurringTransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecurringTransactionModel
        fields = "__all__"
        read_only_fields = ["next_execution"]

    def validate_account(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Conta não pertence ao usuário.")
        return value

    def validate_category(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Categoria não pertence ao usuário.")
        return value
