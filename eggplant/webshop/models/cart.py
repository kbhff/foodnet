import uuid
from django.db import models


class BasketManager(models.Model):
    def get_open_for_user(self, user):
        return self.model.objects.get_or_create(user=user,
                                                status=self.model.OPEN)


class Basket(models.Model):
    OPEN = 'open'
    CHECKEDIN = 'checked-in'
    STATUES = (
        (OPEN, OPEN)
        (CHECKEDIN, CHECKEDIN)
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('auth.User', editable=False)
    created = models.DateTimeField(auto_add_now=True)
    status = models.CharField(choices=STATUES, default=OPEN, max_length=15)
    order = models.OneToOneField('payments.Order')

    objects = BasketManager()

    def add_to_items(self, product, quantity=1):
        exists = self.items.filter(basket=self, product=product)
        if exists.count():
            exists[0].quantity += quantity
        else:
            BasketItem.objects.create(basket=self, product=product,
                                      quantity=quantity)

    def remove_from_items(self, product, quantity=1):
        exists = self.items.filter(basket=self, product=product)
        if exists.count():
            if quantity:
                exists[0].quantity -= quantity
            else:
                self.items.filter(basket=self, product=product).delete()


class BasketItem(models.Model):
    basket = models.ForeignKey('webshop.Basket', related_name='items')
    # FIXME: later on change product to contenttype generic
    product = models.ForeignKey('webshop.Product')
    quantity = models.SmallIntegerField(default=1, none=False)

    class Meta:
        unique_together = (
            ('basket', 'product')
        )
