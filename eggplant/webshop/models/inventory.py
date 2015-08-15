from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(null=False, null=False)


class ProductImage(models.Model):
    product = models.ForeignKey('inventory.Product', null=False)
    name = models.ImageField(upload_to='products')


class Product(models.Model):
    title = models.CharField(null=False, blank=False, max_length=255)
    description = models.TextField(null=False, blank=False)
    category = models.ForeignKey('inventory.ProductCategory', null=True)
    sale_price = models.DecimalField(blank=False, null=False, default=0,
                                     max_digits=5, decimal_places=2)
    tax = models.DecimalField(blank=False, null=False, default=0,
                              max_digits=5, decimal_places=2)
