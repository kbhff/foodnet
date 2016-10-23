from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<role>\w+)/$', views.role, name="role"),
]
