
from django.conf.urls import url

from eggplant.webshop.views import cart as cart_views
from eggplant.webshop.views import inventory as inventory_views


uuid_re_param = '[a-zA-Z0-9]{8}\-?[a-zA-Z0-9]{4}\-?[a-zA-Z0-9]{4}\-?' +\
    '[a-zA-Z0-9]{4}\-?[a-zA-Z0-9]{12}'

urlpatterns = [
    url(r'add-to-cart/$', cart_views.add_to_cart, name="add_to_cart"),
    url(r'remove-from-cart/$', cart_views.remove_from_cart,
        name="remove_from_cart"),
    url(r'your-cart/$',
        cart_views.cart_details, name="cart_details"),
    url(r'checkout/$',
        cart_views.checkout, name="checkout"),
    url(r'$', inventory_views.webshop_home, name="webshop_home"),
]
