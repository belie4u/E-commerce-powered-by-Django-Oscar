from oscar.apps.dashboard.catalogue import forms as base_forms

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
