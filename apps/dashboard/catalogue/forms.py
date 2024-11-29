from oscar.apps.dashboard.catalogue import forms as base_forms
from django import forms
from django.conf import settings
from oscar.apps.dashboard.catalogue.forms import StockRecordForm as CoreStockRecordForm
from apps.catalogue.models import ProductAttribute




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



class ProductAttributesForm(base_forms.ProductAttributesForm):
    product_class_option_names = forms.ChoiceField(
        label="product class option names",
        required=False,
        widget=forms.Select(),
        choices=[]
    )
    class Meta(base_forms.ProductAttributesForm.Meta):
        model = ProductAttribute
        fields = ['name', 'code', 'type', 'variants',
                  'option_group', 'required', "product_class_option_names"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # popurate choices with options if productclass exist 
        product_instance = self.instance if hasattr(self, 'instance') else None
        if product_instance and product_instance.product_class:
            option_names = product_instance.product_class.product_class_option_names
            if option_names:
                self.fields[
                    'product_class_option_names'
                ].choices = [
                    (name,name) for name in option_names
                ]
            else:
                self.fields[
                    "product_class_option_names"
                ].choices = [
                    ('', 'No options available')
                ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_option = self.cleaned_data.get("product_class_option_names")
        if selected_option:
            instance.product_class_option_names = selected_option 
        
        if commit:
            instance.save()

        return instance


class OptionForm(base_forms.OptionForm):

    


    class Meta (base_forms.OptionForm.Meta):
        
        fields = [
            'name', 'type', 'required', 'order', 'help_text', 'option_group', 'is_a_variable_option'
        ]


