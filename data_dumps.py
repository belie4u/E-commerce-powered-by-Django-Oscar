import json
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from oscar.apps.search.facets import base_sqs, FacetMunger

# Initialize base_sqs and facet_munger
sqs = base_sqs()
facet_counts = sqs.facet_counts()
facet_munger = FacetMunger(path='/', selected_multi_facets={}, facet_counts=facet_counts)
facet_data = facet_munger.facet_data()

# Convert translation objects to strings
facet_data_str = {}
for key, value in facet_data.items():
    facet_data_str[str(key)] = str(value)

# Convert facet_data dictionary to JSON format
facet_data_json = json.dumps(facet_data_str, indent=4)

# Write JSON data to a Python file
with open('facet_data.py', 'w') as file:
    file.write("facet_data = ")
    file.write(facet_data_json)
    file.write("\n")

print("Facet data has been written to facet_data.py file.")
