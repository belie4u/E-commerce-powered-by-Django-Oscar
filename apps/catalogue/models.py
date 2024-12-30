
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractAttributeOption, AbstractProductAttribute, AbstractOption, AbstractProductClass
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import (
    ImproperlyConfigured,
    ValidationError,
    ObjectDoesNotExist,
)

from oscar.models.fields import AutoSlugField, NullCharField



class Product(AbstractProduct):
    COLOR_CHOICES = [
        ('green', 'Green'),
        ('grey', 'Grey'),
        ('blue', 'Blue'),
        ('black', 'Black'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('white', 'White'),
        #  Add more choices as needed
    ]

    color = models.CharField(
        max_length=20, choices=COLOR_CHOICES, default='white')
    

class AttributeOption(AbstractAttributeOption):
    icon = models.ImageField(upload_to="attributimages/", blank=True, null=True)



class Option(models.Model):
    """
    An option that can be selected for a particular item when the product
    is added to the basket.

    For example,  a list ID for an SMS message send, or a personalised message
    to print on a T-shirt.

    This is not the same as an 'attribute' as options do not have a fixed value
    for a particular item.  Instead, option need to be specified by a customer
    when they add the item to their basket.

    The `type` of the option determines the form input that will be used to
    collect the information from the customer, and the `required` attribute
    determines whether a value must be supplied in order to add the item to the basket.
    """

    # Option types
    TEXT = "text"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"

    SELECT = "select"
    RADIO = "radio"
    MULTI_SELECT = "multi_select"
    CHECKBOX = "checkbox"
    LOCATIONS = "Locations"
    IMAGE = "Image"

    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (DATE, _("Date")),
        (SELECT, _("Select")),
        (RADIO, _("Radio")),
        (MULTI_SELECT, _("Multi select")),
        (CHECKBOX, _("Checkbox")),
        (LOCATIONS, _("Locations")),
        (IMAGE, _("Image")),
    )

    empty_label = "------"
    empty_radio_label = _("Skip this option")

    name = models.CharField(_("Name"), max_length=128, db_index=True)
    code = AutoSlugField(_("Code"), max_length=128,
                         unique=True, populate_from="name")
    type = models.CharField(
        _("Type"), max_length=255, default=TEXT, choices=TYPE_CHOICES
    )
    is_a_variable_option = models.BooleanField(default=False)
    required = models.BooleanField(
        _("Is this option required?"), default=False)
    option_group = models.ForeignKey(
        "catalogue.AttributeOptionGroup",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="product_options",
        verbose_name=_("Option Group"),
        help_text=_(
            'Select an option group if using type "Option" or "Multi Option"'),
    )
    help_text = models.CharField(
        verbose_name=_("Help text"),
        blank=True,
        null=True,
        max_length=255,
        help_text=_("Help text shown to the user on the add to basket form"),
    )
    order = models.IntegerField(
        _("Ordering"),
        null=True,
        blank=True,
        help_text=_(
            "Controls the ordering of product options on product detail pages"),
        db_index=True,
    )

    @property
    def is_option(self):
        return self.type in [self.SELECT, self.RADIO]

    @property
    def is_multi_option(self):
        return self.type in [self.MULTI_SELECT, self.CHECKBOX, self.LOCATIONS]

    @property
    def is_select(self):
        return self.type in [self.SELECT, self.MULTI_SELECT]

    @property
    def is_radio(self):
        return self.type in [self.RADIO]

    def add_empty_choice(self, choices):
        if self.is_select and not self.is_multi_option:
            choices = [("", self.empty_label)] + choices
        elif self.is_radio:
            choices = [(None, self.empty_radio_label)] + choices
        return choices

    def get_choices(self):
        if self.option_group:
            choices = [
                (opt.option, opt.option) for opt in self.option_group.options.all()
            ]
        else:
            choices = []

        if not self.required:
            choices = self.add_empty_choice(choices)

        return choices

    def clean(self):
        if self.type in [self.RADIO, self.SELECT, self.MULTI_SELECT, self.CHECKBOX, self.LOCATIONS]:
            if self.option_group is None:
                raise ValidationError(
                    _("Option Group is required for type %s") % self.get_type_display()
                )
        elif self.option_group:
            raise ValidationError(
                _("Option Group can not be used with type %s") % self.get_type_display()
            )
        return super().clean()

    class Meta:
        app_label = "catalogue"
        ordering = ["order", "name"]
        verbose_name = _("Option")
        verbose_name_plural = _("Options")

    def __str__(self):
        return self.name











class ProductAttribute(AbstractProductAttribute):
    VARIANTS_CHOICES = [
        ('-----','------'),
        ('colors','Colors'),
        ('materials','Materials')
    ]

    variants = models.CharField(
        choices=VARIANTS_CHOICES,
        default=VARIANTS_CHOICES[0][0],
        max_length=20,
        verbose_name=_("variants")
    )

    product_class_option_names = models.CharField(max_length=50, null=True, blank=True)

class ProductClass (AbstractProductClass):
    @property
    def product_class_option_names (self):
        # retrieves the name of all options related to the product's product class 

        if self.options.exists():
            return [ option.name for option in self.options.all()]
        
        return []




from oscar.apps.catalogue.models import *


