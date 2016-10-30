Developer documentation
=======================

Contents:

.. toctree::
   :maxdepth: 2

   dev/contributing

Component overview
------------------

The Eggplant application contains the following sub-applications (python packages
nested in ``eggplant/`` containing models and migrations).

Applications inside ``eggplant/`` are interdependent, except ``core`` which
should not depend on anything else and ``permissions`` which all other
applications are expected to use.

 - ``accounts`` - Administration and user pages related to accounts, being
   everything that has to do with user's transactions inside the market.
 - ``core`` - an application with models that all other applications may depend
   on, **dependency of others**
 - ``dashboard`` - Functionality for workflow of members, administrators etc.
 - ``departments`` - Administration logic regarding a department such as shifts.
 - ``invitations`` - Sending of invitation emails to create new user profiles
   that join accounts, departments etc.
 - ``membership`` - Extends from Django allauth and contains the models of
   memberships and their organizations.
 - ``market`` - Contains everything related to paying for stuff, invoicing,
   and creating and managing goods such as grocery bags.
 - ``permissions`` - Models and decorators for permissions, **dependency of others**
 - ``profiles`` - User information
 
 
Coupling
~~~~~~~~

Currently, we expect applications to depend on each other's models. But it
would get messy if templates, views, and static assets also started being
interdependent.

Possible scheme: Only allow models and decorators to be interdependent, all
other common elements should live in ``eggplant.core``.

Philosophy
~~~~~~~~~~

To quote Two Scoops of Django (1.8 version) that in turn quotes James Bennett
(who in turn quotes Douglas McIlroy):

    James Bennett volunteers as both a Django core developer and as its release
    manager. He taught us everything that we know about good Django app design.
    We quote him:

        “The art of creating and maintaining a good Django app is that it should
        follow the truncated Unix philosophy according to Douglas McIlroy:
            
            ‘Write programs that do one thing and do it well.’

In essence, each app should be tightly focused on its task. If an app can’t
be explained in a single sentence of moderate length, or you need to say
‘and’ more than once, it probably means the app is too big and should be
broken up.

TODO
~~~~

The scope of the applications may need to be consolidated.

Dependency overview
-------------------

askdasdk
