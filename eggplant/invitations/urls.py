from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'invite/$', views.invite, name="invite"),
    url(r'accept-invitation/(?P<verification_key>[a-z0-9]{32})$',
        views.accept_invitation,
        name="accept_invitation"),
]
