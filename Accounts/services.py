from decimal import Decimal
from django.db import transaction

from currencies.services import convert
from .models import CategoryModel, TransactionModel, TransferModel

from Goals.models import BudgetModel, GoalModel
from Goals.services import recalculate_goal_requirements

@transaction.atomic
def create_transaction(data):
    account = data["account"]
    category = data["category"]
    credit_card = data.get("credit_card")
    amount = Decimal(data["original_amount"])
    tx_type = data["type"]
    tx_date = data["date"]

    original_currency = data.get("original_currency") or account.currency
    converted = convert(amount, original_currency, account.currency)

    if not credit_card:
        if tx_type == "OUT":
            account.current_balance -= converted
        else:
            account.current_balance += converted
        account.save(update_fields=["current_balance"])

    new_transaction = TransactionModel.objects.create(
        account=account,
        credit_card=credit_card,
        category=category,
        original_amount=amount,
        original_currency=original_currency,
        converted_amount=converted,
        status=data.get("status", "COMPLETE"),
        date=tx_date,
        description=data.get("description"),
        type=tx_type,
        is_recurring=data.get("is_recurring", False),
    )

    budget_month = tx_date.month
    budget_year = tx_date.year

    if credit_card:
        from CreditCard.services import get_or_create_invoice
        invoice = get_or_create_invoice(credit_card, tx_date)
        invoice.transactions.add(new_transaction)
        invoice.total_amount += converted
        invoice.save()
        
        budget_month = invoice.due_date.month
        budget_year = invoice.due_date.year

    if tx_type == "OUT":
        budget = BudgetModel.objects.filter(
            user=account.user, 
            category=category, 
            month=budget_month, 
            year=budget_year
        ).first()

        if budget:
            # Soma transações de débito do mês + transações de cartão cuja fatura vence neste mês
            from django.db.models import Sum, Q
            
            total_spent = TransactionModel.objects.filter(
                Q(account__user=account.user, category=category, type='OUT'),
                # Filtro complexo: (Sem cartão e no mês) OU (Com cartão e vencimento da fatura no mês)
                Q(credit_card__isnull=True, date__month=budget_month, date__year=budget_year) |
                Q(credit_card__isnull=False, invoice__due_date__month=budget_month, invoice__due_date__year=budget_year)
            ).distinct().aggregate(Sum('converted_amount'))['converted_amount__sum'] or 0

            if total_spent > budget.amount_limit:
                next_goal = GoalModel.objects.filter(
                    user=account.user, is_completed=False
                ).order_by('deadline').first()
                
                if next_goal:
                    new_burden = recalculate_goal_requirements(next_goal)
                    new_transaction.impact_alert = (
                        f"Orçamento de '{category.name}' estourado! "
                        f"Mês de referência: {budget_month}/{budget_year}. "
                        f"Sua meta '{next_goal.name}' exige {next_goal.currency.symbol} {new_burden:.2f}/mês."
                    )
                    new_transaction.save(update_fields=["impact_alert"])

    return new_transaction

@transaction.atomic
def create_transfer(data):

    source = data["source_account"]
    dest = data["destination_account"]
    amount = Decimal(data["original_amount"])

    original_currency = source.currency

    debited = amount.quantize(Decimal("0.01"))

    credited = convert(amount, original_currency, dest.currency)

    source.current_balance -= debited
    dest.current_balance += credited

    source.save(update_fields=["current_balance"])
    dest.save(update_fields=["current_balance"])

    transfer = TransferModel.objects.create(
        source_account=source,
        destination_account=dest,
        original_amount=amount,
        original_currency=original_currency,
        destination_currency=dest.currency,
        converted_amount=credited,
        date=data["date"]
    )

    transfer_category, _ = CategoryModel.objects.get_or_create(
        name="TRANSFER",
        user=source.user
    )

    TransactionModel.objects.create(
        account=source,
        category=transfer_category,
        original_amount=debited,
        original_currency=source.currency,
        converted_amount=debited,
        status="COMPLETED",
        date=data["date"],
        description="Transferência enviada",
        type="OUT",
        is_recurring=False,
    )

    TransactionModel.objects.create(
        account=dest,
        category=transfer_category,
        original_amount=credited,
        original_currency=dest.currency,
        converted_amount=credited,
        status="COMPLETED",
        date=data["date"],
        description="Transferência recebida",
        type="IN",
        is_recurring=False,
    )

    return transfer
