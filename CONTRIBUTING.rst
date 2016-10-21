============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/kbhff/eggplant/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

eggplant could always use more documentation, whether as part of the
official eggplant docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/kbhff/eggplant/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

.. _getstarted:

Get Started!
------------

Ready to contribute? Here's how to set up `eggplant` for local development.

If you are completely new to source code versioning using git, please search
for a video explaining it. And ask for help getting a git tool set up on your
machine.

.. note:: We have decided to use the very conventional
          `a simple git branching model <https://gist.github.com/jbenet/ee6c9ac48068889b0912>`_.
          Read the guide to get a good introduction to Git workflows.

::

    $ git clone git@github.com:kbhff/eggplant.git

Virtualenv
~~~~~~~~~~

The project is pretty basic, these are classical just steps. Just make note
that it's a Python 3.4 only project. Enter the git project folder.

::

    $ pip install virtualenvwrapper

To get the mkvirtualenv command you need to::

    source  /usr/local/bin/virtualenvwrapper.sh

On debian this file in::

    /etc/bash_completion.d/virtualenvwrapper

start a new bash session to source it.

::

    $ mkvirtualenv eggplantenv -p python3.4
    $ workon eggplantenv
    $ pip install -r requirements/development.txt
    $ python manage.py syncdb
    $ python manage.py runserver

Use "workon eggplantenv" to activate the eggplan virtual environment,
and "deactivate" to exit.

After installing, you probably want a superuser so you can log in. Use
``python manage.py createsuperuser`` to create your first user.

This will deploy a local SQLite database and run a local webserver. If you are
completely new to Django and Python, notice that you need
`pip <https://pip.pypa.io/en/stable/installing/>`_, too.


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.4.
   https://travis-ci.org/kbhff/eggplant/pull_requests
   and make sure that the tests pass for all supported Python versions.


Translation
-----------

As a translator, you can contribute through our
`Transifex project <https://www.transifex.com/kbhff/eggplant/>`__.

Once something has changed, either in the codebase or in Transifex, we use the
Transifex command line client to sync stuff. From within the repo::

    pip install transifex-client  # Installs the client
    tx pull -a  # Pulls all the translation languages
    tx push -s  # Pushes current English source language to Transifex


Tips
----

To run a subset of tests::

    $ python manage.py test --tests=eggplant.profiles.tests.TestProfile

