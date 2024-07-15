
from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractProduct


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
    
from oscar.apps.catalogue.models import *


