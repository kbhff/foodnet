
from django.conf.urls import include, url

from .views import cart, inventory, payment

payment_patterns = [
    url(r'payment-list/$', payment.payment_list, name="payment_list"),

    url(r'payment-detail/(?P<pk>\d+)/$',
        payment.payment_detail,
        name="payment_detail"),

    url(r'payment-info/(?P<pk>\d+)/$',
        payment.payment_info,
        name="order_info"),

    url(r'payment-accepted/(?P<pk>\d+)/$',
        payment.payment_accepted,
        name="payment_accepted"),

    url(r'payment-rejected/(?P<pk>\d+)/$',
        payment.payment_rejected,
        name="payment_rejected"),
]

urlpatterns = [
    url(r'payment/', include(payment_patterns)),
    url(r'add-to-cart/$', cart.add_to_cart, name="add_to_cart"),
    url(r'remove-from-cart/$', cart.remove_from_cart, name="remove_from_cart"),
    url(r'your-cart/$', cart.cart_details, name="cart_details"),
    url(r'checkout/$', cart.checkout, name="checkout"),
    url(r'market/add-product/$', inventory.add_product, name="add_product"),
    url(r'$', inventory.market_home, name="market_home"),
]
