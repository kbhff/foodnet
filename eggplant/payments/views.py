import logging

from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test

from getpaid.forms import PaymentMethodForm

from eggplant.common.views import LoginRequiredMixinView
from eggplant.membership.utils import is_active_account_owner
from .models import Order

log = logging.getLogger(__name__)


@login_required
def payments_home(request):
    return redirect('eggplant:payments:orders_list')


@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    ctx = {
        'orders': orders
    }
    return render(request, 'eggplant/payments/orders_list.html', ctx)


@login_required
def order_info(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    ctx = {
        'orders': [order, ]
    }
    return render(request, 'eggplant/payments/orders_list.html', ctx)


class OrderView(LoginRequiredMixinView, DetailView):
    model = Order

    def get_template_names(self):
        return ['eggplant/payments/order_detail.html', ]

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['payment_form'] = PaymentMethodForm(
            self.object.currency,
            initial={'order': self.object}
        )
        return context

    @method_decorator(
        user_passes_test(is_active_account_owner,
                         login_url='eggplant:payments:payments_home'))
    def dispatch(self, *args, **kwargs):
        return super(OrderView, self).dispatch(*args, **kwargs)
order_detail = OrderView.as_view()


@login_required
@user_passes_test(is_active_account_owner,
                  login_url='eggplant:payments:payments_home')
def payment_accepted(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    messages.info(request, _("Your payment has been accepted and"
                             " it's being processed."))
    return redirect('eggplant:payments:orders_list')


@login_required
@user_passes_test(is_active_account_owner,
                  login_url='eggplant:payments:payments_home')
def payment_rejected(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    messages.error(request, _("Your payment has been cancelled."))
    return redirect("eggplant:payments:orders_list")
