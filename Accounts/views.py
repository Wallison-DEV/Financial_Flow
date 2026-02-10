from django.shortcuts import render
from rest_framework import permissions, viewsets

from .serializers import AccountSerializer, CategorySerializer, TransactionSerlializer, TransferSerializer
from .models import AccountModel, CategoryModel, TransactionModel, TransferModel

class AccountViewSet(viewsets.ModelViewSet):
    queryset = AccountModel.objects.all().order_by('id')
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = TransactionModel.objects.all().order_by('date')
    serializer_class = TransactionSerlializer
    permission_classes = [permissions.IsAuthenticated]

class TransferViewSet(viewsets.ModelViewSet):
    queryset = TransferModel.objects.all().order_by('date')
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]