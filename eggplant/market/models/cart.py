from django.conf import settings

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone
from moneyed import Money

from .payment import Payment, PaymentItem


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

        # sanity check
        if self.status != self.OPEN:
            return

        currency = self.get_currency()
        if currency and currency != product.price.currency:
            raise ValidationError('The products have different currencies')

        current = self.items.filter(product=product, delivery_date=delivery_date).first()

        if current:
                current.quantity += quantity
                current.save()
        else:
            BasketItem.objects.create(
                basket=self,
                product=product,
                quantity=quantity,
                delivery_date=delivery_date
            )

    def remove_from_items(self, product=None, quantity=1, delivery_date=None):

        # sanity check
        if self.status != self.OPEN:
            return

        current = self.items.filter(product=product,
                                    delivery_date=delivery_date).first()
        if current:
            if current.quantity - quantity > 1:
                current.quantity -= quantity
                current.save()
            else:
                self.items.filter(basket=self, product=product, delivery_date=delivery_date).delete()

    def get_total_amount(self):

        if self.get_items_count() == 0:
            return Money(0, getattr(settings, 'DEFAULT_CURRENCY'))

        items = self.items.all().select_related('product')

        total = items[0].product.price * items[0].quantity
        for item in items[1:]:
            total += item.product.price * item.quantity

        return total

    def get_items_count(self):
        return self.items.all().count()

    def get_currency(self):
        item = self.items.first()
        if item:
            return item.product.price.currency
        return None

    @transaction.atomic
    def do_checkout(self):
        # sanity check
        if self.status != self.OPEN:
            return None

        payment = Payment.objects.create(
            amount=self.get_total_amount(),
            # FIXME: get valid account
            user=self.user,
            basket=self
        )
        self.status = self.CHECKEDOUT

        for item in self.items.all():
            PaymentItem.objects.create(
                payment=payment,
                name=item.product.title,
                price=item.product.price,
                quantity=item.quantity,
                delivery_date=item.delivery_date
            )

        self.save()
        return payment.id


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
            ('basket', 'product', 'delivery_date')
        )
        app_label = 'market'
