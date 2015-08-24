
import uuid
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings
import getpaid


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    total = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    currency = models.CharField(max_length=3, default='DKK',
                                choices=settings.CURRENCIES)
    user = models.ForeignKey('auth.User')
    created = models.DateTimeField(auto_now_add=True, null=False,
                                   db_index=True)

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


from .listeners import *
