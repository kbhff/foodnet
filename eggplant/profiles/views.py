import logging
from allauth.account.views import PasswordSetView, sensitive_post_parameters_m, \
    PasswordChangeView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import redirect

from django.views.generic import FormView

from eggplant.core.views import LoginRequiredMixin
from eggplant.profiles.forms import NewUserSetPasswordForm, ProfileForm
from eggplant.profiles.models import UserProfile

logger = logging.getLogger(__name__)


class NewUserPassword(LoginRequiredMixin, PasswordSetView):
    """
    Set password only for a new user. Existing users can use password change.
    """
    success_url = reverse_lazy('eggplant:profiles:profile')
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
        return super(NewUserPassword, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile = self.request.user.profile
        if profile.is_complete() or \
                not request.session.pop('new-invited-user', False):
            # existing user
            msg = "User with completed profile %s is trying to set password."
            logger.warn(msg, self.request.user)
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


class LoginAfterPasswordChange(LoginRequiredMixin, PasswordChangeView):
    """
    After password change, log user out and redirect to account_login.
    """
    success_url = reverse_lazy('account_login')

    def form_valid(self, form):
        ret = super(LoginAfterPasswordChange, self).form_valid(form)
        logout(self.request)
        return ret


class Profile(LoginRequiredMixin, FormView):
    """Profile form view."""
    form_class = ProfileForm
    template_name = 'eggplant/profiles/profile_detail.html'
    success_url = reverse_lazy('eggplant:dashboard:home')

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
        User.objects.filter(id=user_id)\
            .update(first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'])
        del form.cleaned_data['first_name']
        del form.cleaned_data['last_name']
        UserProfile.objects.filter(user_id=user_id).update(**form.cleaned_data)
        msg = "Your profile has been successfully updated."
        messages.success(self.request, msg)
        return super(Profile, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['form'] = kwargs['form']
        return context
