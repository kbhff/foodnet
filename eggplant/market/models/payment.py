import getpaid
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField


class Payment(models.Model):
    amount = MoneyField(
        _("amount to be paid"),
        max_digits=12,
        decimal_places=2,
    )
    account = models.ForeignKey('accounts.Account', null=True)
    created = models.DateTimeField(auto_now_add=True, null=False, db_index=True)
    basket = models.ForeignKey('market.Basket', editable=False, default=None)
    user = models.ForeignKey('auth.User', editable=False, default=None, null=True)

    UNPAID = 'unpaid'
    PAID_CASH = 'paid-cash'
    PAID_MOBILE = 'paid-mobile'
    CANCELED = 'canceled'
    STATUES = (
        (UNPAID, UNPAID),
        (PAID_CASH, PAID_CASH),
        (PAID_MOBILE, PAID_MOBILE),
        (CANCELED, CANCELED),
    )
    status = models.CharField(choices=STATUES, default=UNPAID, max_length=15, null=True)

    extra = models.CharField(
        _("extra information about the payment"),
        max_length=512,
        null=True,
        default=None,
        blank=True
    )

    def get_absolute_url(self):
        return reverse('eggplant:market:payment_detail', args=[str(self.id)])

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


class PaymentItem(models.Model):

    payment = models.ForeignKey('market.Payment', related_name='items')

    name = models.CharField(
        _("product_name"),
        max_length=512
    )

    price = MoneyField(
        _("price"),
        max_digits=12,
        decimal_places=2,
    )

    quantity = models.PositiveSmallIntegerField(default=1, null=False)

    delivery_date = models.DateField(null=True, blank=False)
