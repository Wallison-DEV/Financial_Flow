import uuid
from django.db import models

class CurrencyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=3, unique=True) #BRL, USD, EUR
    name = models.CharField(max_length=50)
    simbol = models.CharField(max_length=5)

    is_base= models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code