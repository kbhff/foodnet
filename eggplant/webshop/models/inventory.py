from django.db import models


class Product(models.Model):
    WEEKLY_BAG = 'weekly bag'
    DRY_GOODS = 'dry goods'
    LOOSE_WEIGHT_VEGETABLES = 'loose weight vegetables'
    DAIRY = 'dairy'
    FEE = 'fee'
    CATEGORY_CHOICES = (
        (WEEKLY_BAG, WEEKLY_BAG),
        (DRY_GOODS, DRY_GOODS),
        (LOOSE_WEIGHT_VEGETABLES, LOOSE_WEIGHT_VEGETABLES),
        (DAIRY, DAIRY),
        (FEE, FEE),
    )
    title = models.CharField(null=False, blank=False, max_length=70)
    description = models.TextField(null=False, blank=False)
    category = models.CharField(null=True, choices=CATEGORY_CHOICES,
                                max_length=50)
    price = models.DecimalField(blank=False, null=False, default=0,
                                max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField(null=False, default=1)
    tax = models.DecimalField(blank=False, null=False, default=0,
                              max_digits=5, decimal_places=2)
    enabled = models.BooleanField(default=True, null=False, blank=False)
    image = models.ImageField(upload_to='products', null=True)

    def __str__(self):
        return "{} {} ({})".format(self.id, self.title, self.category)
