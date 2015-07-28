
| |travisci| |version| |downloads| |supported-versions| |supported-implementations|

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

It's very common to need to extract data from program source.

The problem is that the Python likes to have its text indented means that
literal data would often have extra spaces and lines that you really don't
want. This drives many developers to drop in Python ``list`` data structures
but that's tedious, more verbose, and often less legible.

``textdata`` makes it easy to have clean, nicely-whitespaced data specified
in your program, but to get the data that you want without extra whitespace
cluttering things up. It's permissive of whitespace needed to make the
program source look and work right, yet doesn't require that they they be
seen in the resulting data.

Python string methods give easy ways to clean this text up, but it's no joy
reinventing that particular text-cleanup wheel every time you need
it--especially since many of the details are nitsy, dropping the code down
into low-level constructs rather than just "give me the text!" And because
the details can be a little tricky and frustrating, it's good to not just
whip up some routine *a la carte*, but to use well-tested code.

This module helps clean up included text (or text lines) in a simple,
reusable way that won't muck up your programs with extra code, and won't
require constant wheel-reinvention.

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

If instead you used ``textlines()``, the result is the same, but
joined by newlines into into a single string::

    "There was an old woman who lived in a shoe.\nShe ... to bed."
    # where the ... abbreviates exactly the characters you'd expect

``textlines`` is an optional entry point, as ``lines`` has a ``join``
kwarg that, if set, joins the lines with that string.

Both routines provide typically-desired cleanups:

  * remove blank lines (default), but at least first and last blanks
    (which usually appear due to Python formatting)
  * remove common line prefix (default)
  * strip leading/trailing spaces other than the common prefix
    (leading by request, trailing by default)
  * (optionally) join the lines together with your choice of separator string

The API
=======

``lines(text, noblanks=True, dedent=True, lstrip=False, rstrip=True, join=False)``

    Returns text as a series of cleaned-up lines.

    * ``text`` is the text to be processed.
    * ``noblanks`` => all blank lines are eliminated, not just starting and ending ones. (default ``True``).
    * ``dedent`` => strip a common prefix (usually whitespace) from each line (default ``True``).
    * ``lstrip`` => strip all left (leading) space from each line (default ``False``).
      Note that ``lstrip`` and ``dedent`` are  mutually exclusive ways of handling leading space.
    * ``rstrip`` => strip all right (trailing) space from each line (default ``True``)
    * ``join`` => either ``False`` (do nothing), ``True`` (concatenate lines), or a string that will be used to join the resulting lines (default ``False``)

``textlines(text, noblanks=True, dedent=True, lstrip=False, rstrip=True, join=False)``

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
however, by embedded apostropes and other common gotchas. For example::

    >>> words("don't be blue")
    ["don't", "be", "blue"]

    >>> words(""" "'this'" works '"great"' """)
    ["'this'", 'works', '"great"']

``words`` is a good choice for situations where you want a compact,
friendly, whitespace-delimited data representation--but a few of your
entries need more than just ``str.split()``.

Unicode and Encodings
=====================

.. |star| unicode:: 0x2605 .. star
    :trim:

``textdata`` doesn't have any unique friction with Unicode
characters and encodings, but any time you use Unicode characters
in Python source files--especially in Python 2--care is warranted.

If your text includes Unicode characters, in Python 2 make sure to
mark the string with a "u" prefix: ``u"`` |star| ``"``. You can
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

  * The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_
    or `@jeunice on Twitter <http://twitter.com/jeunice>`_ welcomes
    your comments and suggestions.

Installation
============

::

    pip install -U textdata

To ``easy_install`` under a specific Python version (3.3 in this example)::

    python3.3 -m easy_install --upgrade textdata

(You may need to prefix these with "sudo " to authorize installation.)
