# ...existing code...
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from Goals.models import BudgetModel

class Command(BaseCommand):
    help = "Renova/Cria BudgetModels mensais a partir dos templates/recorrentes"

    def handle(self, *args, **options):
        now = timezone.now()
        month, year = now.month, now.year

        templates = BudgetModel.objects.filter(is_recurring=True)

        with transaction.atomic():
            for tpl in templates.select_for_update():
                existing, created = BudgetModel.objects.select_for_update().get_or_create(
                    user=tpl.user,
                    category=tpl.category,
                    month=month,
                    year=year,
                    defaults={
                        "amount": tpl.amount,
                        "notes": tpl.notes,
                    },
                )

                if not created:
                    existing.save()