
import uuid
from django.core.urlresolvers import reverse
from django.db import models
import getpaid


CURRENCIES = (
    ('DKK', 'DKK'),
    ('PLN', 'PLN'),
    ('GBP', 'GBP'),
)


class OrderManager(models.Manager):

    def create_for_fee(self, user, fee):
        name = "Order for {}".format(fee.name)
        instance = self.model(name=name,
                              total=fee.amount,
                              user=user,
                              currency=fee.currency)
        instance.save()
        return instance


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    total = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    currency = models.CharField(max_length=3, default='DKK',
                                choices=CURRENCIES)
    user = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True, null=False,
                                   db_index=True)

    objects = OrderManager()

    def get_absolute_url(self):
        return reverse('payments:order_info', kwargs={'pk': self.pk})

    def get_last_payment_status(self):
        payments = self.payments.all().order_by('-created_on')[:1]
        if payments:
            return payments[0].status

    def __str__(self):
        return "{} {} ({})".format(
            self.id,
            self.name,
            self.get_last_payment_status()
        )

    def is_ready_for_payment(self):
        return bool(self.total)


Payment = getpaid.register_to_payment(Order, unique=False,
                                      related_name='payments')


class FeeConfig(models.Model):
    ONE_OFF = 'o'
    MONTHLY = 'm'
    QUATERLY = 'q'
    ANNUALLY = 'a'
    APPLICATION_CHOICES = (
        (ONE_OFF, 'one off'),
        (MONTHLY, 'monthly'),
        (QUATERLY, 'quaterly'),
        (ANNUALLY, 'annually'),
    )
    name = models.CharField(max_length=100, null=False, unique=True)
    amount = models.DecimalField(null=False, blank=False, decimal_places=2,
                                 max_digits=8, default=0)
    application = models.CharField(max_length=1, null=False, blank=False,
                                   choices=APPLICATION_CHOICES)
    currency = models.CharField(max_length=3, default='DKK',
                                choices=CURRENCIES)
    enabled = models.BooleanField(default=True, null=False, blank=False)


from .listeners import *
