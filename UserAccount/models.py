from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from currencies.models import CurrencyModel

class UserModel(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="user_model_groups", 
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_model_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

class LanguageChoices(models.TextChoices):
    PT_BR = "pt-BR", "Português (Brasil)"
    EN = "en", "English"

def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)

class ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    default_currency = models.ForeignKey(
        CurrencyModel,
        on_delete=models.PROTECT,
        related_name="profiles"    
    )
    language = models.CharField(max_length=10, choices=LanguageChoices, default=LanguageChoices.PT_BR)
    profile_picture = models.ImageField(upload_to=user_directory_path,null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)