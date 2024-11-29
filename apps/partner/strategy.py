from decimal import Decimal as D

from django.conf import settings

from oscar.apps.partner.strategy import Default as CoreDefault
from oscar.core.loading import get_class

from oscar.apps.partner import strategy

from apps.partner.utils import convert_currency


FixedPrice = get_class('partner.prices', 'FixedPrice')
UnavailablePrice = get_class('partner.prices', 'Unavailable')
TaxInclusiveFixedPrice = get_class('partner.prices', 'TaxInclusiveFixedPrice')

class IncludingVAT(strategy.FixedRateTax):
    rate = D('0.20')


class Default(CoreDefault, IncludingVAT):
    """
    Partner strategy , that convert prices from stockrecord currency
    to user-selected currncy 
    """

    def get_currency(self):
        # check if the request is available and has a session attribute 
        if self.request and hasattr(self.request, 'session'):
            currency = self.request.session.get('currency', None)
        else:
            currency = None
        # default to the default currency if not found in session
        currency = currency  or settings.OSCAR_DEFAULT_CURRENCY
        return currency
    
    def convert_currency (self, stockrecord, prices):
        currency = self.get_currency()
        price_excl_tax = convert_currency(
            stockrecord.price_currency, currency, prices.excl_tax
        )
        return FixedPrice(excl_tax = price_excl_tax, currency=currency, tax=D(0))
    
    def pricing_policy(self, product, stockrecord):
        if not stockrecord or stockrecord.price is None:
            return UnavailablePrice()
        
        # apply default pricing policy 
        price = super().pricing_policy(product, stockrecord)

        # if the stockrecord currency matches the selected currency , apply Vat direclty
        if self.get_currency() == stockrecord.price_currency:
            tax = (price.excl_tax * IncludingVAT.rate).quantize(D('0.01'))
            return TaxInclusiveFixedPrice(
                currency=price.currency,
                excl_tax=price.excl_tax,
                tax = tax
            )
        
        # convert currency if necessary
        converted_price = self.convert_currency(stockrecord, price)
        tax = (converted_price.excl_tax * IncludingVAT.rate).quantize(D('0.01'))
        return TaxInclusiveFixedPrice(
            currency = converted_price.currency,
            excl_tax =converted_price.excl_tax,
            tax = tax
        )

    
    def parent_availability_policy(self, product, children_stock):
        prices = super().parent_availability_policy(product, children_stock)
        if children_stock:
            stockrecord = children_stock[0][1]
            currency = self.get_currency()
            default_excl_tax = D('0.00')
            default_currency = settings.OSCAR_DEFAULT_CURRENCY
            excl_tax = getattr(prices, 'excl_tax', default_excl_tax)
            price_currency = getattr(prices, 'currency', default_currency)
            if currency == stockrecord.price_currency:
                tax = (excl_tax * IncludingVAT.rate).quantize(D('0.01'))
                return TaxInclusiveFixedPrice(
                    currency=price_currency,
                    excl_tax = excl_tax,
                    tax = tax
                )
            price = self.convert_currency(stockrecord, prices)
            tax = (prices.excl_tax * IncludingVAT.rate).quantize(D('0.01'))
            return TaxInclusiveFixedPrice(
                currency = price.currency,
                excl_tax = price.excl_tax,
                tax = tax
            )
        


class Selector(object):
    def strategy(self, request=None, user=None, **kwargs):
        # ensure a strategy is created even f request is none

        return Default(request)