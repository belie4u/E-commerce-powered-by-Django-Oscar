from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from oscar.apps.basket.middleware import BasketMiddleware as CoreBsketMiddleware

from oscar.core.loading import get_model

Basket = get_model ('basket', 'basket')


class BasketMiddleware(CoreBsketMiddleware):

    def get_basket(self, request):
        if request._basket_cache is not None:
            return request._basket_cache
        
        num_basket_merged = 0
        manager = Basket.open
        cookie_key = self.get_cookie_key(request)
        cookie_basket = self.get_cookie_basket(cookie_key, request, manager)

        if hasattr(request, 'user') and request.user.is_authenticated:
            cache_key = f"user_basket_{request.user.id}"
            basket = cache.get(cache_key)
            if basket is None:
                try:
                    basket, created = manager.get_or_create(owner = request.user)
                    if created:
                        basket.currency = request.session.get(
                            'currency', settings.OSCAR_DEFAULT_CURRENCY
                        )
                        basket.save()
                    cache.set(cache_key, basket, 60 * 5)

                except Basket.MultipleObjectsReturned:
                    old_basket = list(manager.filter(owner = request.user ))
                    basket = old_basket[0]
                    for other_basket in old_basket [1:]:
                        self.merge_baskets(basket, other_basket)
                        num_basket_merged += 1

                    basket.owner = request.user
                    cache.set(cache_key, basket, 60 * 5)

            if cookie_basket:
                self.merge_baskets(basket, cookie_basket)
                num_basket_merged += 1
                request.cookies_to_delete.append(cookie_key)

        elif cookie_basket:
            basket = cookie_basket

        else:
            basket = Basket()
        request._basket_cache = basket

        if num_basket_merged > 0:
            messages.add_message(request, messages.WARNING, _(
                "We have merged a basket from a previous session . it might have chenged "
            ))

        return basket
    

    def merge_baskets(self, master_basket, basket_to_merge):
        # only merge if basket_to_merge is not empty

        if not basket_to_merge.is_empty:
            for line in basket_to_merge.all_lines():
                master_basket.merge_line(line)

            basket_to_merge.delete()

        else:
            basket_to_merge.delete()

