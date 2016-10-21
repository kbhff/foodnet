import logging

from allauth.account.models import EmailConfirmation
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from eggplant.profiles.models import UserProfile

log = logging.getLogger(__name__)


class InvitationBackend(ModelBackend):

    def authenticate(self, **credentials):
        """
        Authenticate only invited users with not completed profile.
        """
        User = get_user_model()
        email = credentials.get('email', credentials.get('username'))
        verification_key = credentials.get('password')

        if email:
            users = User.objects.filter(
                email__iexact=email,
                emailaddress__email__iexact=email,
                emailaddress__verified=True
            )
            confirmations_count = EmailConfirmation.objects.filter(
                key=verification_key,
                email_address__verified=True
            ).count()
            if len(users) == 1 and confirmations_count == 1:
                user = users[0]
                try:
                    profile = user.profile
                except UserProfile.DoesNotExist:
                    profile = None
                if not profile.is_complete():
                    return user
                else:
                    log.debug("this is not a new user")
            else:
                msg = "no or too many users or no or too many confirmations"
                log.debug(msg)
        else:
            log.debug("email not found")
