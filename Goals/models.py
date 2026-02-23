from django.db import models
import uuid

from Accounts.models import CategoryModel
from currencies.models import CurrencyModel
from UserAccount.models import UserModel


class GoalModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)

    currency = models.ForeignKey(CurrencyModel, on_delete=models.PROTECT)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)

    account_origin = models.ForeignKey(
        'Accounts.AccountModel', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Conta principal de onde saem os aportes para esta meta."
    )

    # Campo de controle de patrimônio
    is_active = models.BooleanField(default=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BudgetModel(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', 'Essencial'),
        ('MEDIUM', 'Desejável'),
        ('LOW', 'Supérfluo'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT)

    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')

    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('user', 'category', 'month', 'year')