from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum

from .models import GoalModel
from Accounts.models import TransactionModel, CategoryModel

def recalculate_goal_requirements(goal):
    today = date.today()
    remaining_amount = goal.target_amount - goal.current_amount
    
    if remaining_amount <= 0:
        goal.is_completed = True
        goal.save()
        return 0

    delta = relativedelta(goal.deadline, today)
    months_left = max(1, (delta.years * 12) + delta.months) 
    return remaining_amount / months_left

def calculate_monthly_goal_burden(user):
    goals = GoalModel.objects.filter(user=user, is_completed=False)
  
    return sum(recalculate_goal_requirements(g) for g in goals)

@transaction.atomic
def add_goal_deposit(goal, amount, account):
    amount = Decimal(amount)
    
    account.current_balance -= amount
    account.save(update_fields=['current_balance'])
    
    goal.current_amount += amount
    recalculate_goal_requirements(goal) 
    goal.save()

    goal_category, _ = CategoryModel.objects.get_or_create(
        name="Metas", user=goal.user, defaults={'type': 'OUT'}
    )
    TransactionModel.objects.create(
        account=account,
        category=goal_category, 
        original_amount=amount,
        original_currency=account.currency,
        converted_amount=amount,
        type='OUT',
        description=f"Aporte para meta: {goal.name}",
        status='COMPLETE',
        date=timezone.now()
    )
    return goal
