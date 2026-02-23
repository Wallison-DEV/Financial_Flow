from datetime import date, datetime, time
from decimal import Decimal, ROUND_DOWN
from time import timezone
from django.db import transaction
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Q

from .models import CategoryModel, RecurringTransactionModel, TransactionModel, TransferModel
from Goals.models import BudgetModel, GoalModel
from Goals.services import recalculate_goal_requirements
from CreditCard.services import get_or_create_invoice
from currencies.services import convert


def create_installment_schedule(
    account,
    category,
    credit_card,
    amount,
    original_currency,
    tx_date,
    installments,
    tx_type,
    description
):
    base_value = (amount / installments).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    remainder = amount - (base_value * installments)

    created_transactions = []

    for i in range(installments):
        installment_date = tx_date + relativedelta(months=i)

        installment_amount = base_value
        if i == installments - 1:
            installment_amount += remainder

        converted = convert(
            installment_amount,
            original_currency,
            account.currency
        )

        installment_tx = TransactionModel.objects.create(
            account=account,
            credit_card=credit_card,
            category=category,
            original_amount=installment_amount,
            original_currency=original_currency,
            converted_amount=converted,
            status="PENDING",
            date=installment_date,
            description=f"{description} - Parcela {i+1}/{installments}",
            type=tx_type,
            installments=1,
        )

        invoice = get_or_create_invoice(credit_card, installment_date)
        invoice.transactions.add(installment_tx)
        invoice.total_amount += converted
        invoice.save(update_fields=["total_amount"])

        created_transactions.append(installment_tx)

    return created_transactions


@transaction.atomic
def create_transaction(data):
    account = data["account"]
    category = data["category"]
    credit_card = data.get("credit_card")
    installments = data.get("installments", 1)
    amount = Decimal(data["original_amount"])
    tx_type = data["type"]
    tx_date = data["date"]
    description = data.get("description", "")
    original_currency = data.get("original_currency") or account.currency

    if credit_card and installments > 1:
        return create_installment_schedule(
            account=account,
            category=category,
            credit_card=credit_card,
            amount=amount,
            original_currency=original_currency,
            tx_date=tx_date,
            installments=installments,
            tx_type=tx_type,
            description=description
        )
    
    if credit_card and installments == 1:
        converted = convert(amount, original_currency, account.currency)

        transaction = TransactionModel.objects.create(
            account=account,
            credit_card=credit_card,
            category=category,
            original_amount=amount,
            original_currency=original_currency,
            converted_amount=converted,
            status="PENDING",
            date=tx_date,
            description=description,
            type=tx_type,
            installments=1,
        )

        invoice = get_or_create_invoice(credit_card, tx_date)
        invoice.transactions.add(transaction)
        invoice.total_amount += converted
        invoice.save(update_fields=["total_amount"])

        return transaction

    converted = convert(amount, original_currency, account.currency)

    if tx_type == "OUT":
        account.current_balance -= converted
    else:
        account.current_balance += converted

    account.save(update_fields=["current_balance"])

    transaction = TransactionModel.objects.create(
        account=account,
        category=category,
        original_amount=amount,
        original_currency=original_currency,
        converted_amount=converted,
        status="COMPLETE",
        date=tx_date,
        description=description,
        type=tx_type,
        installments=1,
    )

    if tx_type == "OUT":
        budget = BudgetModel.objects.filter(
            user=account.user,
            category=category,
            month=tx_date.month,
            year=tx_date.year
        ).first()

        if budget:
            total_spent = TransactionModel.objects.filter(
                Q(account__user=account.user, category=category, type='OUT'),
                date__month=tx_date.month,
                date__year=tx_date.year
            ).aggregate(Sum('converted_amount'))['converted_amount__sum'] or 0

            if total_spent > budget.amount_limit:
                next_goal = GoalModel.objects.filter(
                    user=account.user,
                    is_completed=False
                ).order_by('deadline').first()

                if next_goal:
                    new_burden = recalculate_goal_requirements(next_goal)
                    transaction.impact_alert = (
                        f"Orçamento de '{category.name}' estourado! "
                        f"Sua meta '{next_goal.name}' exige "
                        f"{next_goal.currency.symbol} {new_burden:.2f}/mês."
                    )
                    transaction.save(update_fields=["impact_alert"])

    return transaction

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
        status="COMPLETE",
        date=data["date"],
        description="Transferência enviada",
        type="OUT",
    )

    TransactionModel.objects.create(
        account=dest,
        category=transfer_category,
        original_amount=credited,
        original_currency=dest.currency,
        converted_amount=credited,
        status="COMPLETE",
        date=data["date"],
        description="Transferência recebida",
        type="IN",
    )

    return transfer

@transaction.atomic
def process_recurring_transactions():
    today = date.today()

    recurrences = RecurringTransactionModel.objects.filter(
        is_active=True,
        next_execution__lte=today
    )

    for recurrence in recurrences:

        execution_datetime = timezone.make_aware(
            datetime.combine(recurrence.next_execution, time.min),
            timezone.get_current_timezone()
        )

        create_transaction({
            "account": recurrence.account,
            "category": recurrence.category,
            "credit_card": recurrence.credit_card,
            "original_amount": recurrence.amount,
            "original_currency": recurrence.currency,
            "type": recurrence.type,
            "date": execution_datetime,
            "description": "Recorrente automática",
            "installments": 1,
        })

        # 🔹 Atualiza próxima execução
        if recurrence.frequency == "DAILY":
            recurrence.next_execution += relativedelta(days=1)

        elif recurrence.frequency == "WEEKLY":
            recurrence.next_execution += relativedelta(weeks=1)

        elif recurrence.frequency == "MONTHLY":
            recurrence.next_execution += relativedelta(months=1)

        elif recurrence.frequency == "YEARLY":
            recurrence.next_execution += relativedelta(years=1)

        if recurrence.end_date and recurrence.next_execution > recurrence.end_date:
            recurrence.is_active = False

        recurrence.save(update_fields=["next_execution", "is_active"])