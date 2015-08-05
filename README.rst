
| |travisci| |version| |downloads| |supported-versions| |supported-implementations| |wheel|

.. |travisci| image:: https://travis-ci.org/jonathaneunice/textdata.svg?branch=master
    :alt: Travis CI build status
    :target: https://travis-ci.org/jonathaneunice/textdata

.. |version| image:: http://img.shields.io/pypi/v/textdata.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/textdata

.. |downloads| image:: http://img.shields.io/pypi/dm/textdata.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/textdata

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/textdata.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/textdata

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/textdata.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/textdata

.. |wheel| image:: https://img.shields.io/pypi/wheel/textdata.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/textdata


Usage
=====

::

    data = lines("""
        There was an old woman who lived in a shoe.
        She had so many children, she didn't know what to do;
        She gave them some broth without any bread;
        Then whipped them all soundly and put them to bed.
    """)

will result in::

    ['There was an old woman who lived in a shoe.',
     "She had so many children, she didn't know what to do;",
     'She gave them some broth without any bread;',
     'Then whipped them all soundly and put them to bed.']

Note that the "extra" newlines and leading spaces have been
taken care of and discarded.

Discussion
==========

One often needs to state data in program source.
Python, however, needs its lines indented *just so*.
Multi-line strings therefore
often have extra spaces and newline characters you didn't really
want. Many developers "fix" this by using Python ``list`` literals,
but that has its own problems: it's tedious, more verbose, and
often less legible.

The ``textdata`` package makes it easy to have clean, nicely-whitespaced
data specified in your program, but to get the data without extra whitespace
cluttering things up. It's permissive of the layouts needed to make Python
code look and work right, without reflecting those requirements in the
resulting data.

Python string methods give easy ways to clean text up, but it's no joy
reinventing that particular wheel every time you need it--especially since
many of the details are nitsy, low-level, and a little tricky. ``textdata``
is a "just give me the text!" module that replaces *a la carte* text
cleanups with simple, well-tested code that doesn't lengthen your program or
require constant wheel-reinvention.

Text
====

In addition to ``lines``, ``textlines`` works similarly and with the same
parametes, but joins the resulting lines into a unified string.::

    data = textlines("""
        There was an old woman who lived in a shoe.
        She had so many children, she didn't know what to do;
        She gave them some broth without any bread;
        Then whipped them all soundly and put them to bed.
    """)

Yields::

    "There was an old woman who lived in a shoe.\nShe ... to bed."
    # where the ... abbreviates exactly the characters you'd expect

API Options
===========

Both ``lines`` and ``textlines`` provide provide routinely-needed cleanups:

  * remove starting and ending blank lines
    (which are usually due to Python source formatting)
  * remove blank lines internal to your text block
  * remove common indentation
  * strip leading/trailing spaces other than the common prefix
    (leading spaces removed by request, trailing by default)
  * strip any comments from the end of lines
  * join lines together with your choice of separator string


``lines(text, noblanks=True, dedent=True, lstrip=False, rstrip=True, join=False)``

    Returns text as a series of cleaned-up lines.

    * ``text`` is the text to be processed.
    * ``noblanks`` => all blank lines are eliminated, not just starting and ending ones. (default ``True``).
    * ``dedent`` => strip a common prefix (usually whitespace) from each line (default ``True``).
    * ``lstrip`` => strip all left (leading) space from each line (default ``False``).
      Note that ``lstrip`` and ``dedent`` are  mutually exclusive ways of handling leading space.
    * ``rstrip`` => strip all right (trailing) space from each line (default ``True``)
    * ``rstrip`` => strip comments (from ``#`` to the end of each line (default ``True``)
    * ``join`` => either ``False`` (do nothing), ``True`` (concatenate lines with ``\n``),
      or a string that will be used to join the resulting lines (default ``False``)

``textlines(text, noblanks=True, dedent=True, lstrip=False, rstrip=True, join='\n')``

    Does the same helpful cleanups as ``lines()``, but returns
    result as a single string, with lines separated by newlines (by
    default) and without a trailing newline.

Words
=====

Often the data you need to encode is almost, but not quite, a series of
words. A list of names, a list of color names--values that are mostly
single words, but sometimes have an embedded spaces. ``textdata`` has you
covered::

    >>> words(' Billy Bobby "Mr. Smith" "Mrs. Jones"  ')
    ['Billy', 'Bobby', 'Mr. Smith', 'Mrs. Jones']

Embedded quotes (either single or double) can be used to construct
"words" (or phrases) containing whitespace (including tabs and newlines).

``words`` isn't a full parser, so there are some extreme cases like
arbitrarily nested quotations that it can't handle. It isn't confused,
however, by embedded apostrophes and other common gotchas. For example::

    >>> words("don't be blue")
    ["don't", "be", "blue"]

    >>> words(""" "'this'" works '"great"' """)
    ["'this'", 'works', '"great"']

``words`` is a good choice for situations where you want a compact,
friendly, whitespace-delimited data representation--but a few of your
entries need more than just ``str.split()``.

Comments
========

If you need to embed more than a few lines of immediate data in your program,
you may want some comments to explain what's going on.  By default,
``textdata`` strip out Python-like comments (from ``#`` to
end of line). So::

    exclude = words("""
        __pycache__ *.pyc *.pyo     # compilation artifacts
        .hg* .git*                  # repository artifacts
        .coverage                   # code tool artifacts
        .DS_Store                   # platform artifacts
    """)

Yields::

    ['__pycache__', '*.pyc', '*.pyo', '.hg*', '.git*',
     '.coverage', '.DS_Store']

You could of course write it out as::

    exclude = [
     '__pycache__', '*.pyc', '*.pyo',   # compilation artifacts
     '.hg*', '.git*',                   # repository artifacts
     '.coverage',                       # code tool artifacts
     '.DS_Store'                        # platform artifacts
    ]

But you'd need more nitsy punctuation.

If however you want to capture
comments, set ``cstrip=False`` (though that is probably more useful with the
``lines`` and ``textlines`` APIs than for ``words``).

Unicode and Encodings
=====================

.. |star| unicode:: 0x2605 .. star
    :trim:

``textdata`` doesn't have any unique friction with Unicode
characters and encodings. That said, any time you use Unicode characters
in Python source files, care is warranted--especially in Python 2!

If your text includes Unicode, in Python 2 make sure to
mark literal strings with a "u" prefix: ``u"`` |star| ``"``. You can
also do this in Python 3.3 and following. Sadly, there was a dropout
of compatibility in early Python 3 releases, making it much harder to
maintain a unified source base with them in the mix. (A
compatibility function such as ``six.u`` from
`six <http://pypi.python.org/pypi/six>`_
can help alleviate much--though certainly not all--of the pain.)

It can also be helpful to declare your source encoding: put
a specially-formatted comment as the first or second line of the source code:

    # -*- coding: <encoding name> -*-

This will usually be ``# -*- coding: utf-8 -*-``, but other encodings are
possible. Python 3 defaults to a UTF-8 encoding, but Python 2 assumes
ASCII.

Notes
=====

  * Version 1.2 adds comment stripping. Packaging and testing also tweaked.

  * Version 1.1.5 adds the ``bdist_wheel`` packaging format.

  * Version 1.1.3 switches from BSD to Apache License 2.0 and integrates
    ``tox`` testing with ``setup.py``.

  * Version 1.1 added the ``words`` constructor.

  * Automated multi-version testing managed with the wonderful
    `pytest <http://pypi.python.org/pypi/pytest>`_,
    `pytest-cov <http://pypi.python.org/pypi/pytest-cov>`_,
    and `tox <http://pypi.python.org/pypi/tox>`_.
    Successfully packaged for, and tested against, all late-model versions of
    Python: 2.6, 2.7, 3.3, 3.4, as well as PyPy 2.5.1 (based on 2.7.9)
    and PyPy3 2.4.0 (based on 3.2.5). Module should work on Python 3.2, but
    dropped from testing matrix due to its age and lack of a Unicode literal
    making test specification much more difficult.)

  * Common line prefix is now computed without considering blank
    lines, so blank lines need not have any indentation on them
    just to "make things work."

  * The tricky case where all lines have a common prefix, but it's
    not entirely composed of whitespace, now properly handled.
    This is useful for lines that are already "quoted" such as
    with leading ``"|"`` or ``">"`` symbols (common in Markdown
    and old-school email usage styles).

  * ``textlines()`` is now somewhat superfluous, now that ``lines()``
    has a ``join`` kwarg.  But you may prefer it for the implicit
    indication that it's turning lines into text.

  * It's tempting to define a constant such as ``Dedent`` that might
    be the default for the ``lstrip`` parameter, instead of having
    separate ``dedent`` and ``lstrip`` Booleans. The more I use
    singleton classes in Python as designated special values, the
    more useful they seem.

  * Automated multi-version testing managed with `pytest
    <http://pypi.python.org/pypi/pytest>`_ and `tox
    <http://pypi.python.org/pypi/tox>`_. Continuous integration testing
    with `Travis-CI <https://travis-ci.org/jonathaneunice/intspan>`_.
    Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

    Successfully packaged for, and
    tested against, all late-model versions of Python: 2.6, 2.7, 3.2, 3.3,
    3.4, and 3.5 pre-release (3.5.0b3) as well as PyPy 2.6.0 (based on
    2.7.9) and PyPy3 2.4.0 (based on 3.2.5).

  * The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_
    or `@jeunice on Twitter <http://twitter.com/jeunice>`_ welcomes
    your comments and suggestions.

Installation
============

To install or upgrade to the latest version::

    pip install -U textdata

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade textdata

(You may need to prefix these with ``sudo`` to authorize
installation. In environments without super-user privileges, you may want to
use ``pip``'s ``--user`` option, to install only for a single user, rather
than system-wide.)
