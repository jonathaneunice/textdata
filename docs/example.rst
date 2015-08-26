A Few Examples
==============

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

In addition to ``lines``, ``textlines`` works similarly and with the same
parameters, but joins the resulting lines into a unified string.::

    data = textlines("""
        There was an old woman who lived in a shoe.
        She had so many children, she didn't know what to do;
        She gave them some broth without any bread;
        Then whipped them all soundly and put them to bed.
    """)

Yields::

    "There was an old woman who lived in a shoe.\nShe ... to bed."
    # where the ... abbreviates exactly the characters you'd expect

Note that while ``textlines`` returns a single string, it
maintains the (useful) newlines. Its result is still line-oriented.
If you want to elide the newlines, use ``textlines(text, join=' ')``
and the newline characters will be replaced with spaces.

