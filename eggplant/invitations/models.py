import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

from eggplant.core.utils import absolute_url_reverse, disable_for_loaddata


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
@disable_for_loaddata
def send_email_invitation(sender, instance, created, **kwargs):
    '''
    TODO: Implement an HTML message, commenting out the html_* lines below
    '''

    department = instance.department.name

    if created:
        subject = _('Your invitation to join the {department} department of {coop_name}!').format(
            department=department,
            coop_name=settings.COOP_NAME
        )
        to_addrs = [instance.email, ]
        invite_url = absolute_url_reverse(
            url_name='eggplant:invitations:accept_invitation',
            kwargs=dict(
                verification_key=instance.verification_key.hex
            )
        )
        context = Context({
            'department': department,
            'coop_name': settings.COOP_NAME,
            'invite_url': invite_url,
        })
        plain_template_path = 'eggplant/invitations/email/department_invitation.txt'
        # html_template_path = 'eggplant/invitations/email/department_invitation.html'
        plain_body = get_template(plain_template_path).render(context)
        # html_body = get_template(html_template_path).render(context)
        send_mail(
            subject,
            plain_body,
            settings.DEFAULT_FROM_EMAIL,
            to_addrs,
            fail_silently=not settings.DEBUG,
            # html_message=html_body
        )
