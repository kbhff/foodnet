# -*- coding: utf-8 -*-
import logging

from django.db import IntegrityError
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import FormView
from django.conf import settings

from allauth.account.models import EmailConfirmation, EmailAddress
from allauth.account.views import sensitive_post_parameters_m,\
    PasswordSetView, PasswordChangeView

from foodnet.common.views import LoginRequiredMixinView
from .forms import (ProfileForm, InviteForm, AcceptInvitationForm,
    NewUserSetPasswordForm)
from .models import Invitation, User, UserProfile, Department
from .utils import create_verified_user


log = logging.getLogger(__name__)


@permission_required('membership.can_invite')
@login_required
def invite(request):
    """Invite a new email address."""
    form = InviteForm()
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            existing_user = User.objects.filter(email=email)
            existing_email = EmailAddress.objects.get_users_for(email=email)
            if existing_user or existing_email:
                msg = 'User {} already exists.'.format(email)
                messages.add_message(request, messages.ERROR, msg)
            else:
                Invitation.objects.create(
                    email=email,
                    invited_by=request.user,
                    department=form.cleaned_data['department'],
                    member_category=form.cleaned_data['member_category'])
                msg = 'Invitation has been send to {}'.format(email)
                messages.add_message(request, messages.SUCCESS, msg)
                return redirect(reverse('home'))
    ctx = {
        'form': form,
        'title': "send invitation",
    }
    return render(request, 'foodnet/membership/invite.html', ctx)


@login_required
def departments_accounts(request, department_name=None):
    # TODO: pagination of user profiles
    assert department_name is not None
    department = Department.objects.get(shortname=department_name)
    user = UserProfile.get_for_user(request.user)
    if not user.has_admin_permission(department=department):
        return HttpResponseForbidden(content="Not a department admin.")

    ctx = {'accounts': department.accounts}
    return render(request, 'foodnet/department/accounts.html', ctx)


@login_required
def admin_profile(request, user_id=None):
    # TODO: actually implement a profile form
    assert user_id is not None
    print("admin_profile edit for {}".format(user_id))
    admin_user = UserProfile.get_for_user(request.user)
    edited_user = UserProfile.objects.get(id=user_id)
    if not edited_user.can_be_edited_by(admin_user):
        return HttpResponseForbidden(content="Current user cannot edit profile")
    return HttpResponse(content="Can edit!")


class AlreadyAcceptedInvitationException(Exception):
    pass


def do_accept_invitation(request, invitation):
    email = invitation.email
    existing_user = User.objects.filter(email=email).exists()
    existing_email = EmailAddress.objects.get_users_for(email=email)
    if existing_user or existing_email:
        msg = "You have already accepted invitation for this email."
        messages.add_message(request, messages.ERROR, msg)
        log.debug("already accepted")
        raise AlreadyAcceptedInvitationException()
    invitation.accepted = True
    invitation.save()
    create_verified_user(invitation)
    # authenticate user via InvitationBackend
    user = authenticate(username=invitation.email,
                        password=invitation.verification_key.hex)
    return user


def accept_invitation(request, verification_key):
    """Accept invitation."""
    if request.user.is_authenticated():
        msg = "You are already logged-in"
        messages.add_message(request, messages.WARNING, msg)
        return redirect(reverse('home'))
    invitation = get_object_or_404(Invitation,
                                   verification_key=verification_key,
                                   accepted=False)
    form = AcceptInvitationForm()
    if request.method == 'POST':
        if settings.USE_RECAPTCHA:
            form = AcceptInvitationForm(request.POST)
            if form.is_valid():
                try:
                    user = do_accept_invitation(request, invitation)
                except AlreadyAcceptedInvitationException:
                    return redirect(reverse('home'))
            else:
                user = None
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
                return redirect(reverse('home'))
        # if this is GET and we use recaptcha just render the form

    if user:
        login(request, user)
        request.session['new-invited-user'] = True
        return redirect(reverse('new_member_set_password'))

    ctx = {
        'form': form,
        'verification_key': verification_key,
        'title': "accept invitation",
    }
    return render(request, 'foodnet/membership/accept_invitation.html', ctx)


class NewUserPasswordView(LoginRequiredMixinView, PasswordSetView):
    """
    Set password only for a new user. Existing users can use password change.
    """
    success_url = reverse_lazy('profile')
    form_class = NewUserSetPasswordForm

    def get_authenticated_redirect_url(self, *args, **kwargs):
        return self.success_url

    def get_success_url(self, *args, **kwargs):
        return self.success_url

    def form_valid(self, form):
        form.save()  # FIXME: password_set signal which redirects to login

    def get(self, request, *args, **kwargs):
        if not request.session.get('new-invited-user'):
            raise Http404()
        return super(NewUserPasswordView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile = UserProfile.get_for_user(self.request.user)
        if profile.is_complete() or \
                not request.session.pop('new-invited-user', False):
            # existing user
            msg = "User with completed profile %s is trying to set password."
            log.warn(msg, self.request.user)
            raise Http404()
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        """Overrides PasswordSetView.dispatch with the View.dispatch"""
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self,
                request.method.lower(),
                self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
sets_new_user_password = NewUserPasswordView.as_view()


class LoginAfterPasswordChangeView(LoginRequiredMixinView, PasswordChangeView):
    """
    After password change redirect to account_login.
    """
    success_url = reverse_lazy('account_login')
loginpage_password_change = LoginAfterPasswordChangeView.as_view()


class ProfileView(LoginRequiredMixinView, FormView):
    """Profile form view."""
    form_class = ProfileForm
    template_name = 'foodnet/membership/profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        self.objects = UserProfile.objects.get(user_id=self.request.user.id)
        return self.objects

    def get_initial(self):
        initial = {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
        }
        initial.update(self.get_object().__dict__)
        return initial

    def form_valid(self, form):
        user_id = self.request.user.id
        profile = UserProfile.get_for_user(self.request.user)
        if not profile.is_complete():
            msg = "Please update your profile."
            messages.add_message(self.request, messages.WARNING, msg)
        User.objects.filter(id=user_id)\
            .update(first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'])
        del form.cleaned_data['first_name']
        del form.cleaned_data['last_name']
        UserProfile.objects.filter(user_id=user_id).update(**form.cleaned_data)
        msg = "Your profile has been successfully updated."
        messages.add_message(self.request, messages.SUCCESS, msg)
        return super(ProfileView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['title'] = 'profile'
        context['form'] = kwargs['form']
        return context
profile = ProfileView.as_view()
