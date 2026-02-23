from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import GoalSerializer, BudgetSerializer
from .models import GoalModel, BudgetModel
from .services import add_goal_deposit

from Accounts.models import AccountModel
from UserAccount.permissions import IsOwner

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = {
        'is_completed': ['exact'],
        'currency': ['exact'],
        'deadline': ['exact', 'gte', 'lte'],  # Ex: ?deadline__gte=2023-01-01
        'target_amount': ['exact', 'gte', 'lte'],
    }
    ordering_fields = ['deadline', 'target_amount', 'current_amount']
    ordering = ['deadline']

    def get_queryset(self):
        return GoalModel.objects.filter(user=self.request.user).order_by('deadline')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        """
        Endpoint: POST /goal/goals/{id}/deposit/
        JSON: {"amount": "100.00", "account_id": "UUID-DA-CONTA"}
        """
        print(f"CONTEÚDO DO JSON: {request.data}") 
        goal = self.get_object()
        amount = request.data.get('amount')
        account_id = request.data.get('account_id')

        if not amount or not account_id:
            return Response({"error": "Informe o valor (amount) e a conta (account_id)"}, status=400)
        
        try:
            account = AccountModel.objects.get(id=account_id, user=request.user)
            update_goal = add_goal_deposit(goal, amount, account)
            
            return Response({
                "status": "Depósito realizado com sucesso",
                "current_amount": update_goal.current_amount,
                "is_completed": update_goal.is_completed
            })
        except AccountModel.DoesNotExist:
            return Response({"error": "Conta de origem não existe"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'month', 'year']

    filterset_fields = {
        'month': ['exact', 'in', 'lte', 'gte'],    # 'in' permite ?month__in=1,2,3
        'year': ['exact', 'in', 'lte', 'gte'],
        'category': ['exact'],
        'priority': ['exact', 'in'],
        'amount_limit': ['gte', 'lte']
    }

    search_fields = ['name', 'category__name']

    ordering_fields = ['month', 'year', 'amount_limit']
    ordering = ['-year', '-month']

    def get_queryset(self):
        return BudgetModel.objects.filter(user=self.request.user).order_by('year')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def carry_over(self, request):
        user = request.user
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        today = date.today()
        last_month_date = today - relativedelta(months=1)
        
        old_budgets = BudgetModel.objects.filter(
            user=user, 
            month=last_month_date.month, 
            year=last_month_date.year
        )
        
        created_count = 0
        for b in old_budgets:
            obj, created = BudgetModel.objects.get_or_create(
                user=user,
                category=b.category,
                month=today.month,
                year=today.year,
                defaults={'amount_limit': b.amount_limit}
            )
            if created: created_count += 1

        return Response({"status": f"{created_count} orçamentos copiados para o mês atual!"})