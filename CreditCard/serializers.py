from rest_framework import serializers

from .models import CreditCardModel, InvoiceModel

class CreditCardSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source='account.name')

    class Meta: 
        model = CreditCardModel
        fields = [
            'id', 'brand', 'limit', 'closing_day', 'due_day', 
            'account', 'account_name', 'currency'
        ]

    def validate_account(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("Você não pode vincular um cartão a uma conta que não é sua.")
        return value

class InvoiceSerializer(serializers.ModelSerializer):
    transactions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = InvoiceModel
        fields = "__all__"
        read_only_fields = ['month', 'year', 'due_date', 'closing_date', 'total_amount']

    def validate_credit_card(self, value):
        if value.account.user != self.context['request'].user:
            raise serializers.ValidationError("Este cartão de crédito não pertence a você.")
        return value