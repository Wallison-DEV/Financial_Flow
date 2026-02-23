from django.core.management.base import BaseCommand
from Accounts.services import process_recurring_transactions


class Command(BaseCommand):
    help = "Processa transações recorrentes pendentes"

    def handle(self, *args, **options):
        process_recurring_transactions()
        self.stdout.write(self.style.SUCCESS("Transações recorrentes processadas com sucesso."))