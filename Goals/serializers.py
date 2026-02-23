from django.db.models import Sum
from rest_framework import serializers

from .models import GoalModel, BudgetModel
from .services import calculate_monthly_goal_burden

from Accounts.models import TransactionModel

class GoalSerializer(serializers.ModelSerializer):
    user =  serializers.PrimaryKeyRelatedField(read_only=True)
    current_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = GoalModel
        fields = ['id', 'user', 'name',  'currency', 'target_amount',
                  'current_amount', 'deadline', 'is_completed']
    
class BudgetSerializer(serializers.ModelSerializer):
    amount_spent = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    is_surplus = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    budget_analysis = serializers.SerializerMethodField()

    class Meta: 
        model = BudgetModel
        fields = ['id', 'user', 'category', 'amount_limit', 'month', 
                  'year', 'amount_spent', 'percentage_used', 'is_surplus',
                  'remaining_amount', 'budget_analysis']
        
    def get_amount_spent(self, obj):
        total = TransactionModel.objects.filter(
            category=obj.category,
            date__month=obj.month,
            date__year=obj.year,
            type='OUT'
        ).aggregate(Sum('converted_amount'))['converted_amount__sum'] or 0 
        return total

    def get_percentage_used(self, obj):
        spent = self.get_amount_spent(obj)
        if obj.amount_limit > 0:
            return round((spent/obj.amount_limit) * 100, 2)
        return 0
    
    def get_remaining_amount(self, obj):
        spent = self.get_amount_spent(obj) 
        return obj.amount_limit - spent

    def get_is_surplus(self, obj):
        return self.get_remaining_amount(obj) < 0
    
    def get_budget_analysis(self, obj):
        user = self.context['request'].user
        profile = getattr(user, 'profilemodel', None)

        if not profile or not profile.monthly_income:
            return "Cadastre sua renda no perfil para análise"
        
        income = profile.monthly_income
        goal_burden = calculate_monthly_goal_burden(user)

        total_budgets = BudgetModel.objects.filter(
            user=user, month=obj.month, year=obj.year
        ).aggregate(Sum('amount_limit'))['amount_limit_sum'] or 0

        available_after_goals = income - goal_burden

        if available_after_goals > 0:
            capacity_percentage = (total_budgets / available_after_goals) * 100
        else:
            capacity_percentage = 100

        if total_budgets > available_after_goals:
            return f"Alerta: Seus orçamentos (R${total_budgets}) superam sua renda disponível após metas (R${available_after_goals:.2f})."
        
        return f"Plano saudável: Você está usando {capacity_percentage:.1f}% da sua renda disponível."

