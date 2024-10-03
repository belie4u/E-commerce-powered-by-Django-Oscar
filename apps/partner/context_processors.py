from .utils import convert_currency

from redpart.settings.base import OSCAR_DEFAULT_CURRENCY




def currency_context(request):
    current_currency = request.session.get('currency', OSCAR_DEFAULT_CURRENCY)

    return {
        'current_currency':current_currency,
        'convert_currency':convert_currency,
    }



def basket_tax_difference(request):
    basket = request.basket
    current_currency = request.session.get(
        'currency', OSCAR_DEFAULT_CURRENCY
    )
    tax_differences =[]

    for line in basket.all_lines():
        unit_price_excl_tax = line.unit_price_excl_tax
        unit_price_incl_tax = line.unit_price_incl_tax

        if unit_price_excl_tax is not None and unit_price_incl_tax is not None:
            tax_difference = unit_price_incl_tax - unit_price_excl_tax
            tax_differences.append({
                'line_id':line.id,
                'tax_difference':tax_difference,
                'currency':current_currency}
            )
        
    return {
        'tax_differences':tax_differences,
    }
