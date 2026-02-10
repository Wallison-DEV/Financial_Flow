from django.db import models
from django.utils.translation import gettext_lazy as _

from Accounts.models import AccountModel, TransactionModel
from currencies.models import CurrencyModel

class CreditCardModel(models.Model):
    account = models.ForeignKey(AccountModel, on_delete=models.PROTECT)
    brand = models.CharField(max_length=20)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    closing_day = models.IntegerField()
    due_day = models.IntegerField()
    currency = models.ForeignKey(CurrencyModel, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InvoiceModel(models.Model):
    class INVOICE_STATUS_CHOICES(models.TextChoices):
        OPEN = "OPEN", _("Aberta")
        CLOSED = "CLOSED", _("Fechada")
        PAID = "PAID", _("Paga")
        PARTIAL = "PARTIAL", _("Parcialmente paga")
        CANCELED = "CANCELED", _("Cancelada")
    credit_card = models.ForeignKey(CreditCardModel, on_delete=models.PROTECT)
    transactions = models.ManyToManyField(TransactionModel, related_name="invoices")
    month = models.IntegerField()
    year = models.IntegerField()
    due_date = models.DateField()
    closing_date = models.DateField()
    currency = models.ForeignKey(CurrencyModel, on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=INVOICE_STATUS_CHOICES.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)