from django import forms

from eggplant.webshop.models.inventory import Product


class BasketItemForm(forms.Form):
    product = forms.ModelChoiceField(Product.objects.filter(stock__gt=0,
                                                            enabled=True))
    quantity = forms.fields.IntegerField(min_value=0, max_value=100,
                                         required=True)
    delivery_date = forms.fields.DateField(required=True)
