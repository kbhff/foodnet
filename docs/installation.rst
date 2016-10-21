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


Fixtures for dev'ing
--------------------

Test/development fixtures in JSON are available in ``fixtures/``::

    python manage.py loaddata fixtures/2016-10-21_exclude_getpaid.json

You can generate new fixtures like this::

    python manage.py dumpdata --natural-primary --natural-foreign --all --indent 4 -e getpaid -e sessions > `date +%F`_exclude_getpaid.json

.. note::
  Fixtures should come with the default superuser:

    - Username: admin
    - Password: admin
    - Email: admin@example.com

.. warning::
  To be nice, remember to clear out the password fields manually before putting
  anything in the repo.

