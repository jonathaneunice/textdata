Installation
============

To install or upgrade to the latest version::

    pip install -U textdata

You make need to use a specific ``pip2`` or ``pip3`` to target
a given version of Python, and on some platforms, you'll need to prefix
the above command with ``sudo`` to authorize installation. 

In environments without super-user privileges, ``pip``'s ``--user`` option 
helps install only for a single user, rather than system-wide.  

If your ``pip`` programs don't seem well configured for the version of Python 
you want, install directly::

    python3.6 -m pip install -U textdata

Testing
-------

If you wish to run the module tests locally, you'll need to install
``pytest`` and ``tox``.  For full testing, you will also need ``pytest-cov``
and ``coverage``. Then run one of these commands::

    tox                # normal run - speed optimized
    tox -e py37        # run for a specific version only (e.g. py27, py36)
    tox -c toxcov.ini  # run full coverage tests
