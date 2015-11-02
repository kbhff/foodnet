from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'', views.Profile.as_view(), name='profile')
]
