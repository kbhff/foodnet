from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


from . import models


class NewUserForceProfileMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.is_superuser:
            allowed_paths = (
                reverse('eggplant:profiles:profile'),
                reverse('account_login'),
                reverse('account_logout'),
                reverse('account_set_password'),
            )
            if request.path not in allowed_paths:
                try:
                    profile = request.user.profile
                except models.UserProfile.DoesNotExist:
                    profile = None
                if not profile or not profile.is_complete():
                    msg = "Please update your profile."
                    messages.add_message(request, messages.WARNING, msg)
                    return HttpResponseRedirect(
                        reverse('eggplant:profiles:profile')
                    )
