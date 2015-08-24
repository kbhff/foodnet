import uuid
from decimal import Decimal

from django.utils import timezone
from django.db import models, transaction


class BasketManager(models.Manager):
    def open_for_user(self, user):
        """
        Get open basket for a given user.
        This is just a wrapper around get_or_create so we can add more
        default kwargs or logic to basket in one place
            - perhaps a check if user payed some fees(?)...
        """
        instance, created = self.get_queryset()\
            .get_or_create(user=user, status=self.model.OPEN)
        return instance


class Basket(models.Model):
    OPEN = 'open'
    CHECKEDOUT = 'checked-out'
    STATUES = (
        (OPEN, OPEN),
        (CHECKEDOUT, CHECKEDOUT),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', editable=False)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUES, default=OPEN, max_length=15)
    order = models.OneToOneField('payments.Order', null=True)

    objects = BasketManager()

    class Meta:
        index_together = [
            ["user", "status"],
        ]

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
        total = Decimal('0')
        for item in self.items.all():
            total += item.quantity * item.product.price
        return total

    def get_items_count(self):
        return self.items.all().count()

    @transaction.atomic
    def do_checkout(self):
        from eggplant.payments.models import Order
        name = "Order for {}".format(self.id)
        order = Order.objects.create(name=name,
                                     total=self.get_total_amount(),
                                     user=self.user,
                                     currency='DKK')
        self.order = order
        self.status = self.CHECKEDOUT
        self.save()


class BasketItem(models.Model):
    basket = models.ForeignKey('webshop.Basket', related_name='items')
    # FIXME: it may be better to have generic contenttype in product...
    product = models.ForeignKey('webshop.Product')
    quantity = models.PositiveSmallIntegerField(default=1, null=False)
    delivery_date = models.DateField(null=False, blank=False,
                                     default=timezone.now)

    class Meta:
        unique_together = (
            ('basket', 'product')
        )
