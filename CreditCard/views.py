from rest_framework import viewsets, permissions

from .models import CreditCardModel, InvoiceModel
from .serializers import CreditCardSerializer, InvoiceSerializer

class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCardModel.objects.all().order_by('brand')
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = InvoiceModel.objects.all().order_by('closing_date')
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]