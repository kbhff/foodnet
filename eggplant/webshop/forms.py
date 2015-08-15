from django import forms

from eggplant.webshop.models.inventory import Product


class BasketItemForm(forms.Form):
    product = forms.ModelChoiceField(Product.objects.all(), required=True)
    quantity = forms.fields.IntegerField(min_value=0, max_value=100)
