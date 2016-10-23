from django.conf.urls import url
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Department

urlpatterns = [
    url(
        r'^$',
        ListView.as_view(
            model=Department,
            template_name='eggplant/departments/department_list.html',
            context_object_name='departments',
        ),
        name='list'
    ),

    url(
        r'^create$',
        CreateView.as_view(
            model=Department,
            template_name='eggplant/departments/department_form.html',
        ),
        name='create'
    ),

    url(
        r'^(?P<slug>\S+)$',
        DetailView.as_view(
            model=Department,
            template_name='eggplant/departments/department_detail.html',
            context_object_name='department',
        ),
        name='detail'
    ),

    url(
        r'^(?P<slug>\S+)/update$',
        UpdateView.as_view(
            model=Department,
            template_name='eggplant/departments/department_form.html',
        ),
        name='update'
    ),

    url(
        r'^(?P<slug>\S+)/delete$',
        DeleteView.as_view(
            model=Department,
            template_name='eggplant/departments/department_delete.html',
            context_object_name='department',
        ),
        name='delete'
    ),
]
