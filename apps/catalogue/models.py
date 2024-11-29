
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractAttributeOption, AbstractProductAttribute, AbstractOption, AbstractProductClass
from django.utils.translation import gettext_lazy as _



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

class Option (AbstractOption):
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
    IMAGE = "image"

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
        (IMAGE, _("Image")),
    )

    is_a_variable_option = models.BooleanField(default=False)

    type = models.CharField(
        _("Type"), max_length=255, default=TEXT, choices=TYPE_CHOICES
    )


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


