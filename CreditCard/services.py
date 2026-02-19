from .models import InvoiceModel

def get_or_create_invoice(credit_card, date):
    invoice, created = InvoiceModel.objects.get_or_create(
        credit_card=credit_card,
        month=date.month,
        year=date.year,
        defaults={
            'due_date': ..., 
            'status': 'OPEN'
        }
    )
    return invoice