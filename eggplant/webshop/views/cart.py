
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render

from eggplant.webshop.models.cart import Basket, BasketItem
from eggplant.webshop.forms import BasketItemForm


class BaseCartActionView(FormView):
    form_class = BasketItem
    success_url = reverse_lazy('webshop:home')

    def form_valid(self, form):
        self.basket = Basket.objects.get_open_for_user(self.request.user)
        return super(BaseCartActionView, self).form_valid(form)


class AddToCart(BaseCartActionView):
    def form_valid(self, form):
        resp = super(BaseCartActionView, self).form_valid(form)
        return resp
add_to_cart = login_required(AddToCart.as_view())


class RemoveFromCart(BaseCartActionView):
    def form_valid(self, form):
        resp = super(BaseCartActionView, self).form_valid(form)
        return resp
remove_from_cart = login_required(RemoveFromCart.as_view())


@login_required
def cart_details(request):
    basket = Basket.objects.get_open_for_user(request.user)
    ctx = {
        'basket': basket,
    }
    return render(request, 'eggplant/webshop/cart_details.html', ctx)
