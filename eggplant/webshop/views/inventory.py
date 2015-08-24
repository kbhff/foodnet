
import logging

from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test

from getpaid.forms import PaymentMethodForm

from eggplant.membership.utils import is_active_account_owner
from eggplant.webshop.models.inventory import Product
from eggplant.webshop.models.cart import Basket


log = logging.getLogger(__name__)


@login_required
def webshop_home(request):
    products = Product.objects.filter(stock__gt=0, enabled=True)
    basket = Basket.objects.open_for_user(request.user)
    all_items = basket.items.all()
    ctx = {
        'basket': basket,
        'basket_items': all_items,
        'products': products
    }
    return render(request, 'eggplant/webshop/webshop_home.html', ctx)
