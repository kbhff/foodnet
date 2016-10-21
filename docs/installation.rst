============
Installation
============

.. warning::
    Eggplant is under heavy development and is not fully fuctional. The point
    of this document is mainly to give a sense of how Eggplant can be used by
    external organizations.

Eggplant is an application for `Django <https://www.djangoproject.com>`_, meaning
that it's something you would embed in a *django project*.

However, for your convenience, it comes with a pre-setup Django project so you
can run it with default settings and templates for development etc. To get started
**developing**, please see :ref:`getstarted`.

In order to install Eggplant for a given other Django project, obtain eggplant
from PyPi::

    $> mkvirtualenv my_eggplant_env
    $> pip install django\>=1.9,\<2.0
    $> django-admin startproject my_eggplat_project
    $> pip install eggplant
    $> $EDITOR my_eggplat_project/settings.py
    $> # INSERT from eggplat.deployments.default.settings.base import *
    $> $EDITOR my_eggplat_project/urls.py
    $> # Insert url(r'^eggplant/', include('eggplant.urls')) in urlpatterns

.. note::
    We haven't released the first eggplant on PyPi yet, so you need to
    get it directly from Github instead

