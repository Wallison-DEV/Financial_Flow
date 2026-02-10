from django.contrib import admin

from . import models

admin.site.register(models.AccountModel)
admin.site.register(models.CategoryModel)
admin.site.register(models.TransferModel)
admin.site.register(models.TransactionModel)