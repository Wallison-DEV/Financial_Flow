import uuid
from django.db import models

class CurrencyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=3, unique=True) #BRL, USD, EUR
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)

    rate_to_base = models.DecimalField(max_digits=12, decimal_places=6)

    is_base= models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} — {self.name} ({self.symbol})"
