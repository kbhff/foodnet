from allauth.account.models import EmailAddress, EmailConfirmation
from django.contrib.auth import get_user_model


def create_verified_user(invitation):
    User = get_user_model()
    # Instead of setting the users password to some UUID hex string.
    # Calling create_user without a password whis will call
    # set_unusable_password() and enable the use of has_usable_password() on
    # the user object.
    user = User.objects.create_user(invitation.email, invitation.email)
    req = None
    email_address = EmailAddress.objects\
        .add_email(req, user, invitation.email, confirm=False, signup=False)
    email_address.verified = True
    email_address.primary = True
    email_address.save()
    econfirm = EmailConfirmation(email_address=email_address,
                                 key=invitation.verification_key.hex)
    econfirm.save()

    return user
