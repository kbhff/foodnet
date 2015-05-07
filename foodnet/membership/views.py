# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from .forms import LoginForm


log = logging.getLogger(__file__)


@sensitive_post_parameters()
@never_cache
def log_in(request):
    """login view"""

    if request.user.is_authenticated():
        msg = 'You are already logged-in.'
        messages.add_message(request, messages.INFO, msg)
        return redirect(reverse('home'))

    ctx = {
        'title': 'Please log-in.',
        'form': LoginForm(),
    }
    if request.method != 'POST':
        return render(request, 'membership/login.html', ctx)

    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(**form.cleaned_data)
        if user is not None:
            if user.is_active:
                # User is valid, active and authenticated
                login(request, user)
                msg = 'You have successfully log-in.'
                messages.add_message(request, messages.INFO, msg)
                return redirect(reverse('home'))
            else:
                msg = 'You email is no longer active.'
                messages.add_message(request, messages.ERROR, msg)
        else:
            msg = 'Incorrect email and/or password.'
            messages.add_message(request, messages.ERROR, msg)
    else:
        msg = 'Invalid email and/or password.'
        messages.add_message(request, messages.ERROR, msg)

    ctx['form'] = LoginForm(request.POST)
    return render(request, 'membership/login.html', ctx)


def log_out(request):
    """logout view"""
    logout(request)
    return redirect(reverse('home'))


@login_required
def profile(request):
    """profile page"""

    ctx = {
        'title': 'profile',
    }
    return render(request, 'membership/profile.html', ctx)
