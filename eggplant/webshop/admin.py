from django.conf import settings
from django.contrib import admin


from .models.inventory import Product
from .models.cart import Basket
admin.site.register(Product)
if settings.DEBUG:
    admin.site.register(Basket)
