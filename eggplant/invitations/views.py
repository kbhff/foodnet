import logging

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render

from eggplant.accounts.models import Account
from eggplant.invitations.models import DepartmentInvitation
from eggplant.invitations.forms import AcceptInvitationForm, \
    DepartmentInvitationForm
from eggplant.invitations.utils import create_verified_user

logger = logging.getLogger(__name__)


class AlreadyAcceptedInvitationException(Exception):
    pass


def do_accept_invitation(request, invitation):
    email = invitation.email
    existing_user = User.objects.filter(email=email).exists()
    existing_email = EmailAddress.objects.get_users_for(email=email)
    if existing_user or existing_email:
        msg = "You have already accepted invitation for this email."
        messages.error(request, msg)
        logger.debug("already accepted")
        raise AlreadyAcceptedInvitationException()
    invitation.accepted = True
    invitation.save()

    with transaction.atomic():
        user = create_verified_user(invitation)
        user.profile.save()
        account = Account.objects.create(
            category=invitation.account_category,
            department=invitation.department
        )
        account.user_profiles.add(user.profile)

    # authenticate user via InvitationBackend
    user = authenticate(username=invitation.email,
                        password=invitation.verification_key.hex)
    return user


def accept_invitation(request, verification_key):
    """Accept invitation."""
    if request.user.is_authenticated():
        msg = "You are already logged-in"
        messages.add_message(request, messages.WARNING, msg)
        return redirect(reverse('eggplant:dashboard:home'))
    invitation = get_object_or_404(DepartmentInvitation,
                                   verification_key=verification_key,
                                   accepted=False)
    form = AcceptInvitationForm()
    user = None
    if request.method == 'POST':
        if settings.USE_RECAPTCHA:
            form = AcceptInvitationForm(request.POST)
            if form.is_valid():
                try:
                    user = do_accept_invitation(request, invitation)
                except AlreadyAcceptedInvitationException:
                    return redirect(reverse('eggplant:dashboard:home'))
            else:
                msg = 'Invalid captcha.'
                messages.add_message(request, messages.WARNING, msg)
        else:
            # If not using recaptcha we don't show
            # the form so there is no POST
            pass
    else:
        if not settings.USE_RECAPTCHA:
            try:
                user = do_accept_invitation(request, invitation)
            except AlreadyAcceptedInvitationException:
                return redirect(reverse('eggplant:dashboard:home'))
                # if this is GET and we use recaptcha just render the form

    if user:
        login(request, user)
        request.session['new-invited-user'] = True
        messages.success(request, 'You have accepted the invitation.')
        return redirect(reverse('account_set_password'))
    ctx = {
        'form': form,
        'verification_key': verification_key,
        'title': "accept invitation",
    }
    return render(request,
                  'eggplant/invitations/accept_invitation.html', ctx)


@permission_required('membership.can_invite')
@login_required
def invite(request):
    """Invite a new email address."""
    form = DepartmentInvitationForm()
    if request.method == 'POST':
        form = DepartmentInvitationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            existing_user = User.objects.filter(email=email)
            existing_email = EmailAddress.objects.get_users_for(email=email)
            if existing_user or existing_email:
                msg = 'User {} already exists.'.format(email)
                messages.error(request, msg)
            else:
                DepartmentInvitation.objects.create(
                    email=email,
                    invited_by=request.user,
                    department=form.cleaned_data['department'],
                    account_category=form.cleaned_data['account_category']
                )
                msg = 'Invitation has been send to {}'.format(email)
                messages.add_message(request, messages.SUCCESS, msg)
                return redirect(reverse('eggplant:dashboard:home'))
    ctx = {
        'form': form,
        'title': "send invitation",
    }
    return render(request,
                  'eggplant/invitations/invite.html', ctx)
