from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from oscar.core.loading import get_model
from django.core.validators import EMPTY_VALUES
from django.forms import widgets   
from oscar.apps.basket.forms import SimpleAddToBasketMixin
from django.forms.widgets import CheckboxSelectMultiple
import ast
from django.utils.encoding import force_str
from django.forms.widgets import MultiWidget, FileInput,TextInput
from oscar.forms.widgets import ImageInput


Basket = get_model('basket', 'Basket')
Option = get_model('catalogue', 'Option')
Product = get_model('catalogue', 'Product')

from oscar.core.loading import get_model

Basket = get_model('basket', 'Basket')

CURRENCY_CHOICES = [('', _('Select currency'))] + \
    [(c,) * 2 for c in settings.OSCAR_CURRENCIES]


class BasketCurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)


def _option_text_field(form, product, option):
    return forms.CharField(
        label=option.name, required=option.required, help_text=option.help_text
    )


def _option_integer_field(form, product, option):
    return forms.IntegerField(
        label=option.name, required=option.required, help_text=option.help_text
    )


def _option_boolean_field(form, product, option):
    return forms.BooleanField(
        label=option.name, required=option.required, help_text=option.help_text
    )


def _option_float_field(form, product, option):
    return forms.FloatField(
        label=option.name, required=option.required, help_text=option.help_text
    )


def _option_date_field(form, product, option):
    return forms.DateField(
        label=option.name,
        required=option.required,
        widget=forms.widgets.SelectDateWidget,
        help_text=option.help_text,
    )


def _option_select_field(form, product, option):
    return forms.ChoiceField(
        label=option.name,
        required=option.required,
        choices=option.get_choices(),
        help_text=option.help_text,
    )


def _option_radio_field(form, product, option):
    return forms.ChoiceField(
        label=option.name,
        required=option.required,
        choices=option.get_choices(),
        widget=forms.RadioSelect,
        help_text=option.help_text,
    )


def _option_multi_select_field(form, product, option):
    return forms.MultipleChoiceField(
        label=option.name,
        required=option.required,
        choices=option.get_choices(),
        help_text=option.help_text,
    )


def _option_checkbox_field(form, product, option):
    return forms.MultipleChoiceField(
        label=option.name,
        required=option.required,
        choices=option.get_choices(),
        widget=forms.CheckboxSelectMultiple,
        help_text=option.help_text,
    )

def _option_file_field(form, product, option):
    return forms.FileField(
        label=option.name,
        required=option.required,
        help_text=option.help_text,
        widget= forms.FileInput()

    )

class LocationWidget(MultiWidget):
    def __init__(self, choices=None, attrs = None):
        widgets = [CheckboxSelectMultiple(choices=choices)]
        widgets.extend([FileInput() for _ in choices])
        widgets.extend([TextInput() for _ in choices])
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if not value or value in EMPTY_VALUES:
            return (
                [[]]
                + [None for _ in self.widgets[1:len(self.widgets) // 2]]
                + ['' for _ in self.widgets[len(self.widgets) // 2:]]

            )

        if isinstance(value,str):
            try:
                dict_value = ast.literal_eval(force_str(value)) 
                return [
                    dict_value.get('selected', []),
                    *[
                        dict_value.get(f'image_{i}', None)
                        for i in range (len(self.widgets) // 2 - 1)
                    ],
                    *[
                        dict_value.get(f'text_{i}', '')
                        for i in range(len(self.widgets) // 2 - 1 )

                    ],

                ]
            except (ValueError, SyntaxError):
                pass

        if isinstance(value, list):
             return value

        return value


class LocationField (forms.MultiValueField):
    def __init__(self, *arg, choices = None , **kwargs):
        fields = [forms.MultipleChoiceField(choices=choices, required=False)]
        fields.extend([forms.ImageField(required=False) for _ in choices])
        fields.extend([forms.CharField(required=False) for _ in choices])
        super().__init__(fields=fields, required_all_fields = False, *arg, **kwargs)


    def compress (self, data_list):
        if data_list:
            data_dict = {
                'selected locations': data_list[0],
                'images':{},
                'texts':{}
            }

            for i, image in enumerate(data_list[1:len(data_list) // 2], start=1):
                if image:
                    data_dict['images'][f'location {i}'] = image.name

            for i, text in enumerate(data_list[len(data_list) // 2:], start = 0):
                if text:
                    data_dict['texts'][f'location {i}'] = text

            return data_dict

        return None


def _option_location_field(form, product, option):
    return LocationField(
        label=option.name,
        required = False,
        widgets = LocationWidget(choices=option.get_choices()),
        help_text = option.help_text,
        choices=option.get_choices(),
    )





class AddToBasketForm(forms.Form):
    OPTION_FIELD_FACTORIES = {
        Option.TEXT: _option_text_field,
        Option.INTEGER: _option_integer_field,
        Option.BOOLEAN: _option_boolean_field,
        Option.FLOAT: _option_float_field,
        Option.DATE: _option_date_field,
        Option.SELECT: _option_select_field,
        Option.RADIO: _option_radio_field,
        Option.MULTI_SELECT: _option_multi_select_field,
        Option.CHECKBOX: _option_checkbox_field,
        Option.IMAGE: _option_file_field,
        Option.LOCATIONS: _option_location_field

    }

    quantity = forms.IntegerField(initial=1, min_value=1, label=_("Quantity"))

    def __init__(self, basket, product, *args, **kwargs):
        # Note, the product passed in here isn't necessarily the product being
        # added to the basket. For child products, it is the *parent* product
        # that gets passed to the form. An optional product_id param is passed
        # to indicate the ID of the child product being added to the basket.
        self.basket = basket
        self.parent_product = product

        super().__init__(*args, **kwargs)

        # Dynamically build fields
        if product.is_parent:
            self._create_parent_product_fields(product)
        self._create_product_fields(product)

    # Dynamic form building methods

    def _create_parent_product_fields(self, product):
        """
        Adds the fields for a "group"-type product (eg, a parent product with a
        list of children.

        Currently requires that a stock record exists for the children
        """
        choices = []
        disabled_values = []
        for child in product.children.public():
            attr_summary = child.attribute_summary or child.get_title()
            info = self.basket.strategy.fetch_for_product(child)

            if not info.availability.is_available_to_buy:
                disabled_values.append(child.id)

            choices.append((child.id, attr_summary))

        self.fields['child_id'] = forms.ChoiceField(
            choices= tuple(choices),
            label=_("variant"),
            widget=widgets.AdvancedSelect(disabled_values=disabled_values)
        )

    def _create_product_fields(self, product):
        """
        Add the product option fields.
        """
        for option in product.options:
            self._add_option_field(product, option)

    def _add_option_field(self, product, option):
        """
        Creates the appropriate form field for the product option.

        This is designed to be overridden so that specific widgets can be used
        for certain types of options.
        """
        if option.type == Option.IMAGE:
            option_field = forms.ImageField(
                widget=ImageInput(),
                label=option.name,
                required=option.required,

            )
        elif option.type == Option.LOCATIONS:
            option_field = _option_location_field(self,product, option)

        else:
            option_field_factory = self.OPTION_FIELD_FACTORIES.get(
                option.type, _option_text_field
            )
            option_field =option_field_factory(self, product, option)

        self.fields[option.code] = option_field

    # Cleaning

    def clean_child_id(self):
        try:
            child = self.parent_product.children.get(
                id=self.cleaned_data["child_id"])
        except Product.DoesNotExist:
            raise forms.ValidationError(_("Please select a valid product"))

        # To avoid duplicate SQL queries, we cache a copy of the loaded child
        # product as we're going to need it later.
        self.child_product = child  # pylint: disable=W0201

        return self.cleaned_data["child_id"]

    def clean_quantity(self):
        # Check that the proposed new line quantity is sensible
        qty = self.cleaned_data["quantity"]
        basket_threshold = settings.OSCAR_MAX_BASKET_QUANTITY_THRESHOLD
        if basket_threshold:
            total_basket_quantity = self.basket.num_items
            max_allowed = basket_threshold - total_basket_quantity
            if qty > max_allowed:
                raise forms.ValidationError(
                    _(
                        "Due to technical limitations we are not able to ship"
                        " more than %(threshold)d items in one order. Your"
                        " basket currently has %(basket)d items."
                    )
                    % {"threshold": basket_threshold, "basket": total_basket_quantity}
                )
        return qty

    @property
    def product(self):
        """
        The actual product being added to the basket
        """
        # Note, the child product attribute is saved in the clean_child_id
        # method
        return getattr(self, "child_product", self.parent_product)

    def clean(self):
        info = self.basket.strategy.fetch_for_product(self.product)

        # Check that a price was found by the strategy
        if not info.price.exists:
            raise forms.ValidationError(
                _(
                    "This product cannot be added to the basket because a "
                    "price could not be determined for it."
                )
            )

        # Check currencies are sensible
        if self.basket.currency and info.price.currency != self.basket.currency:
            raise forms.ValidationError(
                _(
                    "This product cannot be added to the basket as its currency "
                    "isn't the same as other products in your basket"
                )
            )

        # Check user has permission to add the desired quantity to their
        # basket.
        current_qty = self.basket.product_quantity(self.product)
        desired_qty = current_qty + self.cleaned_data.get("quantity", 1)
        is_permitted, reason = info.availability.is_purchase_permitted(
            desired_qty)
        if not is_permitted:
            raise forms.ValidationError(reason)

        return self.cleaned_data

    # Helpers

    def cleaned_options(self):
        """
        Return submitted options in a clean format
        """
        options = []
        for option in self.parent_product.options:
            if option.code in self.cleaned_data:
                value = self.cleaned_data[option.code]
                if option.required or value not in EMPTY_VALUES:
                    options.append({"option": option, "value": value})
        return options
    





class SimpleAddToBasketForm(SimpleAddToBasketMixin, AddToBasketForm):
    """
    Simplified version of the add to basket form where the quantity is
    defaulted to 1 and rendered in a hidden widget

    If you changed `AddToBasketForm`, you'll need to override this class
    as well by doing:

    class SimpleAddToBasketForm(SimpleAddToBasketMixin, AddToBasketForm):
        pass
    """
