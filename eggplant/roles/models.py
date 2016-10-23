from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class RoleAssignment(models.Model):
    PURCHASER = 'purchaser'
    COMMUNICATOR = 'communicator'
    PACKER = 'packer'
    CASHIER = 'cashier'
    ACCOUNTANT = 'accountant'
    ROLE_CHOICES = (
        (PURCHASER, _('purchaser')),
        (COMMUNICATOR, _('communicator')),
        (PACKER, _('packer')),
        (CASHIER, _('cashier')),
        (ACCOUNTANT, _('accountant')),
    )

    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='role_assignments',
        verbose_name=_('user')
    )

    class Meta:
        unique_together = (('user', 'role'), )
        ordering = ('role', )

    def __str__(self):
        return '%s is %s' % (self.user, self.get_role_display())
