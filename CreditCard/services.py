# CreditCard/services.py
from datetime import date
from .models import InvoiceModel

def get_or_create_invoice(credit_card, transaction_date):
    month = transaction_date.month
    year = transaction_date.year
    
    if transaction_date.day > credit_card.closing_day:
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

    invoice, created = InvoiceModel.objects.get_or_create(
        credit_card=credit_card,
        month=month,
        year=year,
        defaults={
            'due_date': date(year, month, credit_card.due_day),
            'closing_date': date(year, month, credit_card.closing_day),
            'status': 'OPEN',
            'total_amount': 0,
            'currency': credit_card.currency
        }
    )
    return invoice
