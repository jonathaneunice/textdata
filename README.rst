
| |travisci| |version| |downloads| |supported-versions| |supported-implementations|

.. |travisci| image:: https://travis-ci.org/jonathaneunice/textdata.png?branch=master
    :alt: Travis CI build status
    :target: https://travis-ci.org/jonathaneunice/textdata

.. |version| image:: http://img.shields.io/pypi/v/textdata.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/textdata

.. |downloads| image:: http://img.shields.io/pypi/dm/textdata.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/textdata

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/textdata.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/textdata

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/textdata.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/textdata

It's very common to need to extract text or text lines from within
program source. The way Python likes to have its text indented,
however, means that there will often be extra spaces appended to
the beginning of each line, as well as possibly extra lines at the
start and end of the text. They're there to make things look and work
right in the program
source, but they're not useful in the resulting data.

Python string methods give easy ways to clean this text up, but
it's no joy reinventing that particular text-cleanup wheel every
time you need it--especially since many of the details are nitsy,
dropping the code down into low-level constructs rather than
just "give me the text!"

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

Both routines provide  typically-desired cleanups:

  * remove blank lines default), but at least first and last blanks
    (which usually appear due to Python formatting)
  * remove common line prefix (default)
  * strip leading/trailing spaces (leading by request, trailing by default)
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

Notes
=====

 *  Automated multi-version testing managed with the wonderful
    `pytest <http://pypi.python.org/pypi/pytest>`_,
    `pytest-cov <http://pypi.python.org/pypi/pytest>`_,
    and `tox <http://pypi.python.org/pypi/tox>`_.
    Successfully packaged for, and tested against, all late-model versions of
    Python: 2.6, 2.7, 3.2, 3.3, 3.4, as well as PyPy 2.5.1 (based on 2.7.9)
    and PyPy3 2.4.0 (based on 3.2.5).

  * Common line prefix is now computed without considering blank
    lines, so blank lines need not have any indentation on them
    just to "make things work."

  * The tricky case where all lines have a common prefix, but it's
    not entirely composed of whitespace, now properly handled.
    This is useful for lines that are already "quoted" such as
    with leading `"|"` or `">"` symbols (common in Markdown
    and old-school email usage styles)/

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
