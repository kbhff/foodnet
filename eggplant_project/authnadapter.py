import logging

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.account.adapter import DefaultAccountAdapter

from eggplant.invitations.models import DepartmentInvitation


log = logging.getLogger(__name__)


class EggplantAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_redirect_url(self, request):
        log.debug("get_email_confirmation_redirect_url")
        return reverse('eggplant:dashboard:home')

    def is_open_for_signup(self, request):
        return settings.SITE_OPEN_FOR_SIGNUP

    def is_email_verified(self, request, email):
        """
        Checks whether or not the email address is already verified
        beyond allauth scope, by having accepted an
        invitation before signing up.
        """
        ret = DepartmentInvitation.objects.filter(
            email__iexact=email,
            accepted=True
        ).count()
        return bool(ret)
