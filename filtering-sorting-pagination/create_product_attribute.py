from oscar.apps.catalogue.models import *

# create the nmaterial attributes


material = AttributeOptionGroup.objects.create(name='material')
color = AttributeOptionGroup.objects.create(name='color')


# Assign options to material option group

AttributeOption.objects.create(
    group= material,
    option= 'Steel'
)
AttributeOption.objects.create(
    group= material,
    option= 'Aluminium'
)
AttributeOption.objects.create(
    group= material,
    option= 'Thorium'
)

# Assign option to color option group

AttributeOption.objects.create(
    group= color,
    option= 'Red'
)
AttributeOption.objects.create(
    group= color,
    option= 'Blue'
)
AttributeOption.objects.create(
    group= color,
    option= 'Green'
)
AttributeOption.objects.create(
    group= color,
    option= 'Black'
)
AttributeOption.objects.create(
    group= color,
    option= 'White'
)


# optional feedback message

print ("AttributeOptionGroup & AttributeOption Added")