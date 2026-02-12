from decimal import Decimal
from django.db import transaction

from currencies.services import convert
from .models import AccountModel, TransactionModel, TransferModel


@transaction.atomic
def create_transaction(data):
    account = data["account"]
    amount = Decimal(data["original_amount"])
    original_currency = data["original_currency"]
    tx_type = data["type"]

    converted = convert(amount, original_currency, account.currency)

    # Atualiza saldo
    if tx_type == "OUT":
        account.current_balance -= converted
    else:
        account.current_balance += converted

    account.save(update_fields=["current_balance"])

    # Cria transação
    return TransactionModel.objects.create(
        account=account,
        category=data["category"],
        original_amount=amount,
        original_currency=original_currency,
        converted_amount=converted,
        status=data.get("status"),
        date=data["date"],
        description=data.get("description"),
        type=tx_type,
        is_recurring=data.get("is_recurring", False),
    )


@transaction.atomic
def create_transfer(data):

    source = data["source_account"]
    dest = data["destination_account"]

    amount = Decimal(data["original_amount"])
    original_currency = data["original_currency"]

    debited = convert(amount, original_currency, source.currency)

    credited = convert(amount, original_currency, dest.currency)

    source.current_balance -= debited
    dest.current_balance += credited

    source.save(update_fields=["current_balance"])
    dest.save(update_fields=["current_balance"])

    return TransferModel.objects.create(
        source_account=source,
        destination_account=dest,
        original_amount=amount,
        original_currency=original_currency,
        destination_currency=dest.currency,
        converted_amount=credited,
        date=data["date"]
    )