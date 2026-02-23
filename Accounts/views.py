from rest_framework import permissions, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from datetime import date

from .serializers import AccountSerializer, CategorySerializer, TransactionSerlializer, TransferSerializer
from .models import AccountModel, CategoryModel, TransactionModel, TransferModel
from .services import create_transaction, create_transfer

from UserAccount.permissions import IsOwner

from Goals.models import GoalModel, BudgetModel
from Goals.services import calculate_monthly_goal_burden
from CreditCard.models import InvoiceModel


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

class DashboardSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        today = date.today()
        profile = getattr(user, 'profilemodel', None)
        
        # 1. SALDO TOTAL (Contas Reais + Metas)
        total_accounts = AccountModel.objects.filter(user=user).aggregate(Sum('current_balance'))['current_balance__sum'] or 0
        total_goals = GoalModel.objects.filter(user=user).aggregate(Sum('current_amount'))['current_amount__sum'] or 0
        
        # 2. DÍVIDA DE CARTÃO (Faturas abertas)
        total_credit_debt = InvoiceModel.objects.filter(
            credit_card__account__user=user, 
            status='OPEN'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # 3. ANÁLISE DE BUDGET (Mês Atual)
        income = profile.monthly_income if profile else 0
        goal_burden = calculate_monthly_goal_burden(user)
        
        total_budgeted_out = BudgetModel.objects.filter(
            user=user, month=today.month, year=today.year, category__type='OUT'
        ).aggregate(Sum('amount_limit'))['amount_limit__sum'] or 0

        # 4. RESULTADO CONSOLIDADO
        net_worth = (total_accounts + total_goals) - total_credit_debt
        safe_to_spend = income - (total_budgeted_out + goal_burden)

        return Response({
            "net_worth": net_worth,
            "liquid_cash": total_accounts,
            "saved_in_goals": total_goals,
            "credit_card_debt": total_credit_debt,
            "monthly_planning": {
                "income": income,
                "goal_contributions": goal_burden,
                "budget_limits": total_budgeted_out,
                "safe_margin": safe_to_spend,
                "health_status": "HEALTHY" if safe_to_spend > 0 else "DEFICIT"
            },
            "urgent_alerts": self.get_alerts(user, today)
        })

    def get_alerts(self, user, today):
        # Busca orçamentos estourados para avisar no topo do app
        surplus_budgets = BudgetModel.objects.filter(
            user=user, month=today.month, year=today.year
        )
        alerts = []
        for b in surplus_budgets:
            # Reutiliza a lógica do Serializer que já criamos
            if b.amount_limit < self.get_spent(b):
                alerts.append(f"Orçamento de {b.category.name} excedido!")
        return alerts
