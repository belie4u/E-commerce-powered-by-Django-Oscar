
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractAttributeOption


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

from oscar.apps.catalogue.models import *


