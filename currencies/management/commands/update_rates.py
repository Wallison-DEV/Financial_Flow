from django.core.management.base import BaseCommand
import requests
from currencies.models import CurrencyModel

CURRENCY_META = {
    "BRL": {"name": "Real Brasileiro", "symbol": "R$"},
    "USD": {"name": "Dólar Americano", "symbol": "$"},
    "EUR": {"name": "Euro", "symbol": "€"},
    "GBP": {"name": "Libra Esterlina", "symbol": "£"},
    "JPY": {"name": "Iene Japonês", "symbol": "¥"},
    "ARS": {"name": "Peso Argentino", "symbol": "$"},
    "CAD": {"name": "Dólar Canadense", "symbol": "$"},
    "AUD": {"name": "Dólar Australiano", "symbol": "$"},
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        response = requests.get("https://open.er-api.com/v6/latest/BRL")
        data = response.json()

        rates = data.get("rates")

        if not rates:
            self.stderr.write("Erro ao buscar taxas")
            return

        for code, meta in CURRENCY_META.items():

            rate = rates.get(code)

            if not rate:
                continue

            CurrencyModel.objects.update_or_create(
                code=code,
                defaults={
                    "name": meta["name"],
                    "symbol": meta["symbol"],
                    # INVERTE A TAXA
                    "rate_to_base": 1 / rate,
                    "is_base": code == "BRL"
                }
            )

        # garante BRL = 1
        CurrencyModel.objects.filter(code="BRL").update(rate_to_base=1)

        self.stdout.write(self.style.SUCCESS("Main currencies updated successfully"))
