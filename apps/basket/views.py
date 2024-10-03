from django.http import HttpResponseRedirect
from django.views.generic import FormView

from oscar.core.loading import get_class
from django.core.cache import cache


BasketCurrencyForm = get_class('basket.forms', 'BasketCurrencyForm' )


class BasketCurrencyUpdateView(FormView):
    form_class = BasketCurrencyForm

    def form_valid(self, form):
        currency = form.cleaned_data['currency']
        self.request.session['currency'] = currency
        basket = self.request.basket

        # change the basket currency and handle caching

        basket.change_currency(currency)
        cache_key = f'basket_{basket.owner_id}_{currency}'
        # invalidate the cache when the basket change 
        cache.delete(cache_key)

        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')
    
