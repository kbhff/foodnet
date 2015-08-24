
from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import JsonResponse

from eggplant.webshop.models.cart import Basket
from eggplant.webshop.models.inventory import Product
from eggplant.webshop.forms import BasketItemForm


class BaseCartActionView(FormView):
    form_class = BasketItemForm
    success_url = reverse_lazy('eggplant:webshop:webshop_home')

    def get_template_names(self):
        return ['', ]

    def form_valid(self, form):
        self.basket = Basket.objects.open_for_user(self.request.user)
        return super(BaseCartActionView, self).form_valid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)


class AddToCart(BaseCartActionView):
    def form_valid(self, form):
        max_items = getattr(settings, 'WEBSHOP_MAX_ITEMS_IN_BASET', 20)
        with transaction.atomic():
            super().form_valid(form)
            if self.basket.get_items_count() >= max_items:
                msg = _("You are not allowed to have more "
                        "than %d items in your basket.") % (max_items)
                messages.warning(self.request, msg)
                return redirect('eggplant:webshop:webshop_home')
            self.basket.add_to_items(**form.cleaned_data)
            stock = form.cleaned_data['product'].stock - \
                form.cleaned_data['quantity']
            Product.objects.filter(id=form.cleaned_data['product'].id)\
                   .update(stock=stock)
        msg = _("You have just added %s to your basket.") %\
            (form.cleaned_data['product'].title)
        messages.info(self.request, msg)
        return redirect('eggplant:webshop:webshop_home')
add_to_cart = login_required(AddToCart.as_view())


class RemoveFromCart(BaseCartActionView):
    def form_valid(self, form):
        with transaction.atomic():
            super().form_valid(form)
            self.basket.remove_from_items(**form.cleaned_data)
            stock = form.cleaned_data['product'].stock + \
                form.cleaned_data['quantity']
            Product.objects.filter(id=form.cleaned_data['product'].id)\
                   .update(stock=stock)
        return redirect('eggplant:webshop:cart_details')
remove_from_cart = login_required(RemoveFromCart.as_view())


@login_required
def cart_details(request):
    basket = Basket.objects.open_for_user(request.user)
    ctx = {
        'basket': basket,
        'items': basket.items.all(),
    }
    return render(request, 'eggplant/webshop/cart_details.html', ctx)


@login_required
def checkout(request):
    basket = get_object_or_404(Basket, user=request.user, status=Basket.OPEN)

    items = basket.items.all()
    if items.count() < 1:
        return redirect('eggplant:webshop:webshop_home')

    if request.method == 'POST':
        basket.do_checkout()
        return redirect('eggplant:payments:order_detail',
                        pk=str(basket.order.id))

    ctx = {
        'basket': basket,
        'items': items,
    }
    return render(request, 'eggplant/webshop/checkout.html', ctx)
