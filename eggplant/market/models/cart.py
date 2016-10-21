from decimal import Decimal

from django.db import models, transaction
from django.utils import timezone


class BasketManager(models.Manager):
    def open_for_user(self, user):
        """
        Get open basket for a given user.
        This is just a wrapper around get_or_create so we can add more
        default kwargs or logic to basket in one place - perhaps a check if user payed some fees(?)...
        """
        instance, __ = self.get_queryset()\
            .get_or_create(user=user, status=self.model.OPEN)
        return instance


class Basket(models.Model):
    OPEN = 'open'
    CHECKEDOUT = 'checked-out'
    STATUES = (
        (OPEN, OPEN),
        (CHECKEDOUT, CHECKEDOUT),
    )
    user = models.ForeignKey('auth.User', editable=False)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUES, default=OPEN, max_length=15)

    objects = BasketManager()

    class Meta:
        index_together = [
            ["user", "status"],
        ]
        app_label = 'market'

    def __str__(self):
        return 'Basket {} {} {}'.format(self.user, self.status, self.created)

    def add_to_items(self, product=None, quantity=1, delivery_date=None):
        current = self.items.filter(product=product,
                                    delivery_date=delivery_date)
        if current.count():
            current[0].quantity += quantity
            current[0].save()
        else:
            BasketItem.objects.create(
                basket=self,
                product=product,
                quantity=quantity,
                delivery_date=delivery_date
            )

    def remove_from_items(self, product=None, quantity=1, delivery_date=None):
        current = self.items.filter(product=product,
                                    delivery_date=delivery_date)
        if current.exists():
            if current[0].quantity > 1:
                current[0].quantity -= quantity
                current[0].save()
            else:
                self.items.filter(basket=self, product=product).delete()

    def get_total_amount(self):
        # TODO: This should return a Money type instead of decimal
        # TODO: When calculating this, we should fail when currencies differ
        total = Decimal('0')
        for item in self.items.all():
            total += item.quantity * item.product.price.amount
        return total

    def get_items_count(self):
        return self.items.all().count()

    @transaction.atomic
    def do_checkout(self):
        # TODO: Why on earth are we importing this here
        from .payment import Payment
        Payment.objects.create(
            amount=self.get_total_amount(),
            user=self.user,
        )
        # self.order = payment
        self.status = self.CHECKEDOUT
        self.save()


class BasketItem(models.Model):
    basket = models.ForeignKey('market.Basket', related_name='items')
    # FIXME: it may be better to have generic contenttype in product...
    product = models.ForeignKey('market.Product')
    quantity = models.PositiveSmallIntegerField(default=1, null=False)

    # TODO:This is not the way to do it,we should have delivery dates specified
    # on the products themselves -- they are not to be decided by the member
    # but are preconfigured

    # Ignoring Delivery date: https://github.com/kbhff/eggplant/issues/114
    delivery_date = models.DateField(null=True, blank=False,
                                     default=timezone.now)

    class Meta:
        unique_together = (
            ('basket', 'product')
        )
        app_label = 'market'
