from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from Goals.models import BudgetModel
from Accounts.models import CategoryModel  
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Garante que existam budgets para o mês atual"

    def handle(self, *args, **options):
        now = timezone.now()
        month, year = now.month, now.year

        users = User.objects.all()
        categories = CategoryModel.objects.all()

        created_count = 0

        with transaction.atomic():
            for user in users:
                for category in categories:

                    _, created = BudgetModel.objects.get_or_create(
                        user=user,
                        category=category,
                        month=month,
                        year=year,
                        defaults={
                            "amount_limit": 0,
                            "priority": 1,
                        },
                    )

                    if created:
                        created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Budgets garantidos para {month}/{year}. Criados: {created_count}"
            )
        )