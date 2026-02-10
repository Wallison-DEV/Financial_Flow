from rest_framework import serializers

from .models import CreditCardModel, InvoiceModel

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CreditCardModel
        fields = "__all__"

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceModel
        fields = "__all__"