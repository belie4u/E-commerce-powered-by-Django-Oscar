from oscar.apps.dashboard.catalogue import forms as base_forms
from django import forms
from django.conf import settings
from oscar.apps.dashboard.catalogue.forms import StockRecordForm as CoreStockRecordForm




CURRENCY_CHOICES = [(c,)*2 for c in settings.OSCAR_CURRENCIES]


class ProductForm(base_forms.ProductForm):
    class Meta(base_forms.ProductForm.Meta):
        fields = (
            'title',
            'upc',
            'color',
            "description",
            "is_public",
            "is_discountable",
            "structure",
            "slug",
            "meta_title",
            "meta_description",
        )


class AttributeOptionForm(base_forms.AttributeOptionForm):
    class Meta(base_forms.AttributeOptionForm.Meta):
        fields = ("option", "icon")

