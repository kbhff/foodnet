import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

log = logging.getLogger(__file__)


@login_required
def home(request):
    """home page"""
    ctx = {}
    return render(request, 'eggplant/dashboard/home.html', ctx)
