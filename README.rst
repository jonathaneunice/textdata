
| |travisci| |version| |downloads| |versions| |impls| |wheel| |coverage|

.. |travisci| image:: https://travis-ci.org/jonathaneunice/textdata.svg?branch=master
    :alt: Travis CI build status
    :target: https://travis-ci.org/jonathaneunice/textdata

.. |version| image:: http://img.shields.io/pypi/v/textdata.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/textdata

.. |downloads| image:: http://img.shields.io/pypi/dm/textdata.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/textdata

.. |versions| image:: https://img.shields.io/pypi/pyversions/textdata.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/textdata

.. |impls| image:: https://img.shields.io/pypi/implementation/textdata.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/textdata

.. |wheel| image:: https://img.shields.io/pypi/wheel/textdata.svg
    :alt: Wheel packaging support
    :target: https://pypi.python.org/pypi/textdata

.. |coverage| image:: https://img.shields.io/badge/test_coverage-100%25-6600CC.svg
    :alt: Test line coverage
    :target: https://pypi.python.org/pypi/textdata

One often needs to state data in program source. Python, however, needs its
lines indented *just so*. Multi-line strings therefore often have extra
spaces and newline characters you didn't really want. Many developers "fix"
this by using Python ``list`` literals, but that's
tedious, verbose, and often less legible.

The ``textdata`` package makes it easy to have clean, nicely-whitespaced
data specified in your program, but to get the data without extra whitespace
cluttering things up. It's permissive of the layouts needed to make Python
code look and work right, without reflecting those requirements in the
resulting data. For example::

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
taken care of and discarded. Or do you want that as just one
string? Okay::

    data = text("""
        There as an old woman...
                                         ...put them to bed.
    """)

Does the same stripping of pointless whitespace at the beginning
and end, returning the data as a clean, convenient string. Or if you don't
want most of the line endings, try ``textline`` on the same input
to get a single no-breaks line.

Other times, the data you need is almost, but not quite, a series of
words. A list of names, a list of color names--values that are mostly
single words, but sometimes have an embedded spaces. ``textdata`` has you
covered::

    >>> words(' Billy Bobby "Mr. Smith" "Mrs. Jones"  ')
    ['Billy', 'Bobby', 'Mr. Smith', 'Mrs. Jones']

Embedded quotes (either single or double) can be used to construct
"words" (or phrases) containing whitespace (including tabs and newlines).

``words``, like the other ``textdata`` facilities, allows you to
comment individual lines that would otherwise muck up string literals::

    exclude = words("""
        __pycache__ *.pyc *.pyo     # compilation artifacts
        .hg* .git*                  # repository artifacts
        .coverage                   # code tool artifacts
        .DS_Store                   # platform artifacts
    """)

Yields::

    ['__pycache__', '*.pyc', '*.pyo', '.hg*', '.git*',
     '.coverage', '.DS_Store']

Finally, you might wan to collect "paragraphs"--contiguous runs of text lines
that are delineated by blank lines. Markdown and RST document formats,
for example, use this convention.  ``textdata`` makes it easy::

    >>> rhyme = """
        Hey diddle diddle,

        The cat and the fiddle,
        The cow jumped over the moon.
        The little dog laughed,
        To see such sport,

        And the dish ran away with the spoon.
    """
    >>> paras(rhyme)
    [['Hey diddle diddle,'],
     ['The cat and the fiddle,',
      'The cow jumped over the moon.',
      'The little dog laughed,',
      'To see such sport,'],
     ['And the dish ran away with the spoon.']]

Or if you'd like paras, but each paragraph in a single string::

    >>> paras(rhyme, join="\n")
    ['Hey diddle diddle,',
     'The cat and the fiddle,\nThe cow jumped over the moon.\nThe little dog laughed,\nTo see such sport,',
     'And the dish ran away with the spoon.']


``textdata`` is all about conveniently grabbing the data you want
from text files and program source, and doing it in a highly
functional, well-tested way.
Take it for a spin today!

See `the full documentation
at Read the Docs <http://textdata.readthedocs.org/en/latest/>`_.
