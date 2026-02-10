from django.db import migrations

def criar_moedas_padrao(apps, schema_editor):
    Currency = apps.get_model('currencies', 'CurrencyModel')
    
    moedas = [
        {'code': 'BRL', 'name': 'Real Brasileiro', 'symbol': 'R$', 'is_base': True},
        {'code': 'USD', 'name': 'Dólar Americano', 'symbol': 'US$', 'is_base': False},
        {'code': 'EUR', 'name': 'Euro', 'symbol': '€', 'is_base': False},
    ]

    for moeda in moedas:
        Currency.objects.get_or_create(code=moeda['code'], defaults=moeda)

class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(criar_moedas_padrao),
    ]
