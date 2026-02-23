from decimal import Decimal
from django.db import transaction
from Accounts.models import CategoryModel
from Goals.models import BudgetModel
from datetime import date

@transaction.atomic
def setup_initial_user_data(user, monthly_income, currency):
    from .models import ProfileModel
    profile, created = ProfileModel.objects.get_or_create(
        user=user,
        defaults={
            'monthly_income': Decimal(str(monthly_income)),
            'default_currency': currency
        }
    )

    default_categories = {
        ("Aluguel/Moradia", "OUT", 0.30, "HIGH"),
        ("Alimentação", "OUT", 0.15, "HIGH"),
        ("Transporte", "OUT", 0.10, "MEDIUM"),
        ("Lazer", "OUT", 0.05, "LOW"),
        ("Salário Mensal", "IN", 1.0, "HIGH"),
    }

    today = date.today()

    for name, cat_type, percent, priority in default_categories: 
        limit = (Decimal(str(monthly_income)) * Decimal(str(percent)) if cat_type == "OUT" else Decimal(str(monthly_income)))

        category = CategoryModel.objects.create(
            user=user,
            name=name,
            type=cat_type,
            sugested_limit=limit
        )

        BudgetModel.objects.create(
            user=user,
            category=category,
            amount_limit=limit,
            priority=priority,
            month=today.month,
            year=today.year,
        )

    return profile