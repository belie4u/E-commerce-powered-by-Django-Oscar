from decimal import Decimal as D, ROUND_HALF_UP
import requests
from django.core.cache import cache
from django.db import transaction
from apps.partner.models import ExchangeRate
from redpart.settings.base import OSCAR_CURRENCIES

EXCHANGERATES_API_URL = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_kCNbWlbu0hfTntUBKVGGpG9Vuk483bdlQatioFuB"
EXCHANGE_RATE_CACHE_PREFIX = 'exchange_rate_{}:{}'


def fetch_exchange_rates(base_currency, currencies):
    url = f"{EXCHANGERATES_API_URL}&base_currency={
        base_currency}&currencies={','.join(currencies)}"

    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        rates_to_update = []

        for currency, rate in data['data'].items():
            rate = D(rate)  # Convert rate to decimal
            cache_key = EXCHANGE_RATE_CACHE_PREFIX.format(
                base_currency, currency)
            # Set cache with expiration time
            cache.set(cache_key, rate, timeout=3600)
            rates_to_update.append(ExchangeRate(
                base_currency=base_currency,
                currency=currency,
                value=rate
            ))

        with transaction.atomic():
            ExchangeRate.objects.bulk_create(
                rates_to_update, ignore_conflicts=True)

        return data

    except requests.RequestException as e:
        # Handle request exception (e.g., log error)
        return None


def convert_currency(from_currency, to_currency, convertible_value):
    allowed_currencies = set(OSCAR_CURRENCIES)
    if from_currency not in allowed_currencies or to_currency not in allowed_currencies:
        raise ValueError(f"Currency conversion only allowed for {allowed_currencies}")
                         

    cache_key = EXCHANGE_RATE_CACHE_PREFIX.format(from_currency, to_currency)
    rate_value = cache.get(cache_key)

    if rate_value is None:
        fetch_exchange_rates(from_currency, allowed_currencies)
        rate_value = cache.get(cache_key) 

    # Convert convertible value to decimal
    convertible_value = D(convertible_value)

    # Perform currency conversion with rounding
    converted_value = (rate_value * convertible_value).quantize(D('0.01'), ROUND_HALF_UP)
        
        

    return converted_value
