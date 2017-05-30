Notes
=====

* Those who like how ``textdata`` simplifies data extraction from
  text should also consider `quoter <http://pypi.python.org/pypi/quoter>`_,
  a module with the same philosophy about wrapping text and
  joining composite data into strings.

* Automated multi-version testing managed with the wonderful
  `pytest <http://pypi.python.org/pypi/pytest>`_,
  `pytest-cov <http://pypi.python.org/pypi/pytest-cov>`_,
  `coverage <http://pypi.python.org/pypi/coverage>`_,
  and `tox <http://pypi.python.org/pypi/tox>`_.
  Continuous integration testing
  with `Travis-CI <https://travis-ci.org/jonathaneunice/textdata>`_.
  Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

* Successfully packaged for, and
  tested against, all late-model versions of Python: 2.6, 2.7, 3.3,
  3.4, 3.5, and 3.6, as well as recent versions of PyPy and PyPy3.

* It's tempting to define a constant such as ``Dedent`` that might
  be the default for the ``lstrip`` parameter, instead of having
  separate ``dedent`` and ``lstrip`` Booleans. The more I use
  singleton classes in Python as designated special values, the
  more useful they seem.

* The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_
  or `@jeunice on Twitter <http://twitter.com/jeunice>`_ welcomes
  your comments and suggestions.
