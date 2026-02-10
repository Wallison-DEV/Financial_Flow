from django.db import models
from django.utils.translation import gettext_lazy as _

from UserAccount.models import UserModel
from currencies.models import CurrencyModel

class AccountModel(models.Model):
    class ACCOUNT_TYPE_CHOICES(models.TextChoices):
        CHECKING_ACCOUNT ="CC", _("Conta corrente")
        SAVINGS_ACCOUNT ="CP", _("Conta poupança")

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices=ACCOUNT_TYPE_CHOICES.choices)
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    currency = models.ForeignKey(CurrencyModel, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("user", "name")

class TransferModel(models.Model):
    source_account= models.ForeignKey(AccountModel, related_name="outgoing", on_delete=models.PROTECT)
    destination_account = models.ForeignKey(AccountModel, related_name="incoming", on_delete=models.PROTECT)
    date = models.DateTimeField()
    original_amount = models.DecimalField(max_digits=12, decimal_places=2)
    original_currency = models.ForeignKey(CurrencyModel, on_delete=models.PROTECT)
    destination_currency = models.ForeignKey(
        CurrencyModel,
        on_delete=models.PROTECT,
        related_name="transfer_destination_currency"
    )
    converted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CategoryModel(models.Model):
    class CATEGORY_TYPE_CHOICES(models.TextChoices):
        IN = "IN", _("Entrada")
        OUT = "OUT", _("Saída")

    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=3, choices=CATEGORY_TYPE_CHOICES.choices, default=CATEGORY_TYPE_CHOICES.IN)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="children", on_delete=models.PROTECT)
    icon = models.ImageField(upload_to="categories/", null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True) # Hexadecimal color code
    ordering = models.IntegerField(default=0) # Campo para definir a ordem das categorias
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TransactionModel(models.Model):
    class TRANSACTION_TYPE_CHOICES(models.TextChoices):
        COMPLETE = "COMPLETE", _("Completa")
        PENDING = "PENDING", _("Pendente")
        CANCELED = "CANCELED", _("Cancelada")

    account = models.ForeignKey(AccountModel, on_delete=models.PROTECT)
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT)
    original_amount = models.DecimalField(max_digits=12, decimal_places=2)
    original_currency = models.ForeignKey(CurrencyModel, on_delete=models.PROTECT)
    converted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES.choices, default=TRANSACTION_TYPE_CHOICES.PENDING)
    date = models.DateTimeField()
    description = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=3, choices=CategoryModel.CATEGORY_TYPE_CHOICES.choices)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)