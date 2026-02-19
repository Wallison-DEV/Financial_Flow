from rest_framework import permissions, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import AccountSerializer, CategorySerializer, TransactionSerlializer, TransferSerializer
from .models import AccountModel, CategoryModel, TransactionModel, TransferModel

from UserAccount.permissions import IsOwner

from .services import create_transaction, create_transfer

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['type', 'is_active']

    def get_queryset(self):
        return AccountModel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get_queryset(self):
        return CategoryModel.objects.filter(user=self.request.user).order_by('name')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerlializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'date': ['gte', 'lte'], # gte = Greater Than or Equal | lte = Less Than or Equal
        'category': ['exact'],
        'account': ['exact'],
        'status': ['exact'],
        'type': ['exact'],
    }

    search_fields = ['description', 'category__name']

    ordering_fields = ['date', 'original_amount']
    ordering = ['-date']

    def get_queryset(self):
        return TransactionModel.objects.select_related(
            'account', 
            'category', 
            'original_currency'
        ).filter(account__user=self.request.user)
    
    def perform_create(self, serializer):
        create_transaction(serializer.validated_data)

class TransferViewSet(viewsets.ModelViewSet):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'date': ['gte', 'lte'], # gte = Greater Than or Equal | lte = Less Than or Equal
        'source_account': ['exact'],
        'destination_account': ['exact'],
    }

    def get_queryset(self):
        return TransferModel.objects.filter(source_account__user=self.request.user)

    def perform_create(self, serializer):
        create_transfer(serializer.validated_data)