A Few Examples
==============

.. code-block:: pycon

    >>> lines("""
    ...     There was an old woman who lived in a shoe.
    ...     She had so many children, she didn't know what to do;
    ...     She gave them some broth without any bread;
    ...     Then whipped them all soundly and put them to bed.
    ... """)
    ['There was an old woman who lived in a shoe.',
     "She had so many children, she didn't know what to do;",
     'She gave them some broth without any bread;',
     'Then whipped them all soundly and put them to bed.']

Note that the "extra" newlines and leading spaces have been
taken care of and discarded.

In addition to ``lines``, ``text`` works similarly and with the same
parameters, but joins the resulting lines into a unified string.::

.. code-block:: pycon

    >>> text("""
    ...     There was an old woman who lived in a shoe.
    ...     She had so many children, she didn't know what to do;
    ...     She gave them some broth without any bread;
    ...     Then whipped them all soundly and put them to bed.
    ... """)

    "There was an old woman who lived in a shoe.\nShe ...put them to bed."

(Where the ... abbreviates exactly the characters you'd expect.)

So it does the same stripping of pointless whitespace at the beginning and
end, returning the data as a clean, convenient string.

Note that while ``text`` returns a single string, it maintains the
(potentially useful) newlines. Its result is still line-oriented by default.
If you want to elide the newlines, use ``text(text, join=' ')`` and the
newline characters will be replaced with spaces.

A ``textline`` call makes this even easier. It gives a single, no-breaks
string by default. It's particularly useful for rendering single, very long
lines.

