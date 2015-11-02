Developer documentation
=======================

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

TODO
~~~~

The scope of the applications may need to be consolidated.

Dependency overview
-------------------

askdasdk