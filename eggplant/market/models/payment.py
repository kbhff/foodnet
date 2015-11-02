from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djmoney.models.fields import MoneyField

import getpaid


class Payment(models.Model):
    amount = MoneyField(
        _("amount to be paid"),
        max_digits=12,
        decimal_places=2,
    )
    account = models.ForeignKey('accounts.Account')
    created = models.DateTimeField(auto_now_add=True, null=False,
                                   db_index=True)

    def get_absolute_url(self):
        return reverse('eggplant:market:order_info', kwargs={'pk': self.pk})

    def get_last_payment_status(self):
        payments = self.payments.all().order_by('-created_on')[:1]
        if payments:
            return payments[0].status

    def __str__(self):
        return "Payment#{} of {} ({})".format(
            self.id,
            self.amount,
            self.get_last_payment_status(),
        )

    def is_ready_for_payment(self):
        return bool(self.total)

    class Meta:
        app_label = 'market'


GetPaidPayment = getpaid.register_to_payment(
    Payment,
    unique=False,
    related_name='payments'
)
