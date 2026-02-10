from django.db import models
from django.contrib.auth.models import AbstractUser
from currencies.models import CurrencyModel

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class LanguageChoices(models.TextChoices):
    PT_BR = "pt-BR", "Português (Brasil)"
    EN = "en", "English"

class ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    default_currency = models.ForeignKey(
        CurrencyModel,
        on_delete=models.PROTECT,
        related_name="profiles"    
    )
    language = models.CharField(max_length=10, choices=LanguageChoices, default=LanguageChoices.PT_BR)
    profile_picture = models.ImageField(upload_to="profiles/",null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)