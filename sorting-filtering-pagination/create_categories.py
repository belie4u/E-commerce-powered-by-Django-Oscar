from oscar.apps.catalogue.categories import create_from_breadcrumbs

#define the categories list 

categories = [
    'Headlights & Lighting > Turn Signals',
    'Headlights & Lighting > Fog Lights',
    'Headlights & Lighting > Headlights > Lights',

    'Interial Parts > Floor Mats',
    'Interial Parts > Gauges',
    'Interial Parts > steering wheels',
    'Interial Parts > cargo Accessories',

    'Repair Manual',
    'Fuel System',
]


for breadcrumbs in categories:
    create_from_breadcrumbs(breadcrumbs)

print ("categories succesfuly  added")