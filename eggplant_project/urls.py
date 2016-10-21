# -*- coding: utf-8 -*-
import eggplant.profiles.views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.views import logout
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # allauth signup is disabled - we have our own signup flow
    url(r'^account/signup/$',
        RedirectView.as_view(url='eggplant:profiles:signup', permanent=True),
        name='account_signup'),
    # override django-allauth password set and change views
    url(r'^account/password/set/$',
        eggplant.profiles.views.NewUserPassword.as_view(),
        name='account_set_password'),
    # override django-allauth logout so no confirmation is needed
    # see: http://www.sarahhagstrom.com/2013/09/the-missing-django-allauth-tutorial/#Remove_the_logout-confirmation_step
    url(r'^account/logout/$',
        logout,
        {'next_page': '/'}),
    url(r'^getpaid/', include('getpaid.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^', include('eggplant.urls', namespace='eggplant')),
]

urlpatterns = i18n_patterns(*urlpatterns)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
