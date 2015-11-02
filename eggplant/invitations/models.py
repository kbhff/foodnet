import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from eggplant.core.utils import absolute_url_reverse


class InvitationBase(models.Model):
    email = models.EmailField(null=False, blank=False, unique=False)
    accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True)
    verification_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=False,
        unique=True,
    )
    created = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey('auth.User')

    class Meta:
        abstract = True
        permissions = (
            ("can_invite", "Can send invitation"),
        )


class DepartmentInvitation(InvitationBase):
    department = models.ForeignKey('departments.Department')
    account_category = models.ForeignKey('accounts.AccountCategory')

    def __str__(self):
        if self.accepted:
            acp = 'accepted'
        else:
            acp = 'NOT accepted'
        return '{} {}'.format(self.email, acp)


@receiver(
    post_save,
    sender=DepartmentInvitation,
    dispatch_uid='membership-invitation-send_email_invitation'
)
def send_email_invitation(sender, instance, created, **kwargs):

    department = instance.department.name

    if created:
        subject = _('You have been invited to join {department}!').format(
            department=department
        )
        to_addrs = [instance.email, ]
        invite_url = absolute_url_reverse(
            url_name='eggplant:invitations:accept_invitation',
            kwargs=dict(
                verification_key=instance.verification_key.hex
            )
        )
        body = _(
            """Hi there!\n"""
            """Thank you for signing up as a member for {department}. We're """
            """happy that you want to be part of our community.\n"""
            """\n"""
            """Please click the following link to confirm you email address """
            """and fill out your membership details:\n"""
            """{invite_url}\n"""
            """\n"""
            """\n"""
            """Cheers,\n"""
            """all of us at {department}"""
        ).format(invite_url=invite_url, department=department)
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            to_addrs,
            fail_silently=not settings.DEBUG
        )
