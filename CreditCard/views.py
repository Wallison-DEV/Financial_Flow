from rest_framework import viewsets, permissions, mixins

from UserAccount.permissions import IsOwner

from .models import CreditCardModel, InvoiceModel
from .serializers import CreditCardSerializer, InvoiceSerializer

class CreditCardViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return CreditCardModel.objects.select_related('account', 'currency').filter(
            account__user=self.request.user
        ).order_by('brand')

class InvoiceViewSet(mixins.RetrieveModelMixin, 
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin, 
                     viewsets.GenericViewSet):
    
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return InvoiceModel.objects.select_related('credit_card', 'currency').filter(
            credit_card__account__user=self.request.user
        ).order_by('-year', '-month')
