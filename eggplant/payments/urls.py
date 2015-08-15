
from django.conf.urls import url

from eggplant.payments import views

uuid_re_param = '[a-zA-Z0-9]{8}\-?[a-zA-Z0-9]{4}\-?[a-zA-Z0-9]{4}\-?' +\
    '[a-zA-Z0-9]{4}\-?[a-zA-Z0-9]{12}'

urlpatterns = [
    url(r'payments-fees-orders/$', views.payments_home, name="payments_home"),
    url(r'fees-list/$', views.fees_list, name="fees_list"),
    url(r'orders-list/$', views.orders_list, name="orders_list"),

    url(r'order-for-fee/(?P<fee_id>[0-9]{1,10})/$',
        views.create_order_for_fee,
        name="create_order_for_fee"),

    url(r'order-detail/(?P<pk>' + uuid_re_param + ')/$',
        views.order_detail,
        name="order_detail"),

    url(r'order-info/(?P<pk>' + uuid_re_param + ')/$',
        views.order_info,
        name="order_info"),

    url(r'payment-accepted/(?P<pk>' + uuid_re_param + ')/$',
        views.payment_accepted,
        name="payment_accepted"),

    url(r'payment-rejected/(?P<pk>' + uuid_re_param + ')/$',
        views.payment_rejected,
        name="payment_rejected"),
]
