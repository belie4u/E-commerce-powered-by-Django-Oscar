from oscar.apps.partner.models import *
from django.db import models


class ExchangeRate(models.Model):
    base_currency = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=20, decimal_places=6)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s to %s' % (self.base_currency, self.currency)
    
    class Meta:
        unique_together = ("base_currency", "currency")
        indexes = [
            models.Index(fields=["base_currency", "currency"]),
        ]


from oscar.apps.partner.models import *
