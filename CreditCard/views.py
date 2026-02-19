from rest_framework import viewsets, permissions, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend

from UserAccount.permissions import IsOwner

from .models import CreditCardModel, InvoiceModel
from .serializers import CreditCardSerializer, InvoiceSerializer

class CreditCardViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    search_fields = ['brand']
    
    filterset_fields = ['account', 'currency']

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

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'credit_card': ['exact'],
        'status': ['exact'],
        'month': ['exact'],
        'year': ['exact'],
        'due_date': ['gte', 'lte'],
    }
    
    ordering_fields = ['year', 'month', 'due_date']
    ordering = ['-year', '-month']


    def get_queryset(self):
        return InvoiceModel.objects.select_related('credit_card', 'currency').filter(
            credit_card__account__user=self.request.user
        ).order_by('-year', '-month')
