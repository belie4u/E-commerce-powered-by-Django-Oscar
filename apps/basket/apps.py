from django.urls import re_path
import oscar.apps.basket.apps as apps


class BasketConfig(apps.BasketConfig):
    label = 'basket'
    name = 'apps.basket'
    verbose_name = 'Cart'

    def get_urls(self):
        from .views import BasketCurrencyUpdateView
        urls = super().get_urls()
        urls += [
            re_path(
                r'^set_currency/$', BasketCurrencyUpdateView.as_view(), name='basket-currency'
            )
        ]
        return self.post_process_urls(urls)
