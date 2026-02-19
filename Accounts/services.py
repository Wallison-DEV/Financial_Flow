from decimal import Decimal
from django.db import transaction

from currencies.services import convert
from .models import AccountModel, CategoryModel, TransactionModel, TransferModel

@transaction.atomic
def create_transaction(data):
    account = data["account"]
    amount = Decimal(data["original_amount"])
    tx_type = data["type"]

    original_currency = data.get("original_currency") or account.currency

    converted = convert(amount, original_currency, account.currency)

    if tx_type == "OUT":
        account.current_balance -= converted
    else:
        account.current_balance += converted

    account.save(update_fields=["current_balance"])

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
