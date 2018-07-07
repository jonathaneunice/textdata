Lines and Text
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

API Options
-----------

Both ``lines`` and ``text`` provide provide routinely-needed cleanups:

* remove starting and ending blank lines
  (which are usually due to Python source formatting)
* remove blank lines internal to your text block
* remove common indentation
* strip leading/trailing spaces other than the common prefix
  (leading spaces removed by request, trailing by default)
* strip any comments from the end of lines
* join lines together with your choice of separator string


``lines(source, noblanks=True, dedent=True, lstrip=False, rstrip=True, cstrip=True, join=False)``

Returns text as a series of cleaned-up lines.

* ``source`` is the text to be processed. It can be presented as a single string, or as a list of lines.
* ``noblanks`` => all blank lines are eliminated, not just starting and ending ones. (default ``True``).
* ``dedent`` => strip a common prefix (usually whitespace) from each line (default ``True``).
* ``lstrip`` => strip all left (leading) space from each line (default ``False``).
    Note that ``lstrip`` and ``dedent`` are  mutually exclusive ways of handling leading space.
* ``rstrip`` => strip all right (trailing) space from each line (default ``True``)
* ``cstrip`` => strip comments (from ``#`` to the end of each line (default ``True``)
* ``join`` => either ``False`` (do nothing), ``True`` (concatenate lines with ``\n``),
    or a string that will be used to join the resulting lines (default ``False``)

``text(source, noblanks=True, dedent=True, lstrip=False, rstrip=True, cstrip=True, join='\n')``

    Does the same helpful cleanups as ``lines()``, but returns
    result as a single string, with lines separated by newlines (by
    default) and without a trailing newline.

.. note:: Text cleanups inherently convert tabs to sequences of spaces,
    consistent with Python's ``str.expandtabs``. There is currently no option
    to turn this behavior off.