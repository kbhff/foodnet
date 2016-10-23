from django import forms
from django.forms import ModelForm
from eggplant.core.widgets import MoneyWidget

from .models.inventory import Product


class BasketItemForm(forms.Form):
    product = forms.ModelChoiceField(Product.objects.all())
    quantity = forms.fields.IntegerField(min_value=0, max_value=100,
                                         required=True)
    delivery_date = forms.fields.DateField(required=False)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'tax', 'stock']
        widgets = {'price': MoneyWidget()}
