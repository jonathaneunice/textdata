Installation
============

To install or upgrade to the latest version::

    pip install -U textdata

You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide. Sometimes you need to use ``pip2`` or ``pip3`` to install
under a given version of Python. If your ``pip`` programs don't seem well
configured for the version of Python you want, you can install directly::

    python3.6 -m pip install -U textdata

Testing
-------

If you wish to run the module tests locally, you'll need to install
``pytest`` and ``tox``.  For full testing, you will also need ``pytest-cov``
and ``coverage``. Then run one of these commands::

    tox                # normal run - speed optimized
    tox -e py27        # run for a specific version only (e.g. py27, py34)
    tox -c toxcov.ini  # run full coverage tests
