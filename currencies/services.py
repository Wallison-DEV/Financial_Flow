from decimal import Decimal

def convert(amount: Decimal, from_currency, to_currency):

    if from_currency == to_currency:
        return amount.quantize(Decimal("0.01"))

    amount_in_brl = amount * Decimal(from_currency.rate_to_base)

    result = amount_in_brl / Decimal(to_currency.rate_to_base)

    return result.quantize(Decimal("0.01"))

