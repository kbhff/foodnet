# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from foodnet.dashboard import views as dashboard_views
from foodnet.membership import views


urlpatterns = [
    url(r'invite/$', views.invite, name="invite"),
    url(r'accept-invitation/(?P<verification_key>[a-z0-9]{32})$',
        views.accept_invitation,
        name="accept_invitation"),
    url(r'profile/$', views.profile, name="profile"),

    # signup is disabled - we only allow invited users
    url(r'^accounts/signup/$',
        dashboard_views.home,
        name='account_signup'),

    # override password set and change views
    url(r'^accounts/password/change/$',
        views.loginpage_password_change,
        name='account_change_password'),

    url(r'^accounts/password/set/$',
        views.sets_new_user_password,
        name='new_member_set_password'),

    url(r'^departments/(?P<department_name>[\w\d\-]{1,10})/accounts$',
        views.departments_accounts,
        name='department_accounts'),

    url(r'^accounts/', include('allauth.urls')),
]
