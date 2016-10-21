from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from getpaid.admin import PaymentAdmin

from .models import GetPaidPayment, Payment
from .models.cart import Basket
from .models.inventory import Product, ProductCategory, ProductTax

try:
    admin.site.register(GetPaidPayment, PaymentAdmin)
except AlreadyRegistered:
    pass

admin.site.register(Payment)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'stock', 'price', 'enabled')
    list_filter = ('enabled', 'category__title')

admin.site.register(Product, ProductAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'enabled')
    list_filter = ('enabled', )

admin.site.register(ProductCategory, ProductCategoryAdmin)

admin.site.register(ProductTax)

if settings.DEBUG:
    admin.site.register(Basket)
