from django.db import models
from oscar.apps.basket.abstract_models import AbstractBasket
from oscar.core.utils import get_default_currency
from django.core.cache import cache



class Basket(AbstractBasket):
    _currency = models.CharField(max_length=3, default=get_default_currency)

    @property
    def currency(self):
        return self._currency
    
    @currency.setter
    def currency(self, value):
        self._currency = value

    def change_currency(self, currency):
        self.currency = currency
        self.save()

        for line in self.lines.all().select_related('product'):
            stock_info = self.get_stock_info(line.product, options=None)
            line.price_currency = currency
            line.price_excl_tax = stock_info.price.excl_tax
            line.price_incl_tax = stock_info.price.incl_tax
            line.save()

        self.reset_offer_applications()
        cache_key = f'basket_{self.owner_id}_{currency}'
        cache.delete(cache_key)




from oscar.apps.basket.models import * 
