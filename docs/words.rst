Words
=====

Often the data you need to encode is almost, but not quite, a series of
words. A list of names, a list of color names--values that are mostly
single words, but sometimes have an embedded spaces.

.. code-block:: pycon

    >>> words(' Billy Bobby "Mr. Smith" "Mrs. Jones" ')
    ['Billy', 'Bobby', 'Mr. Smith', 'Mrs. Jones']

Embedded quotes (either single or double) can be used to construct
"words" (really, phrases) containing whitespace (including tabs
and newlines).

``words`` isn't a full parser, so there are some extreme cases like
arbitrarily nested quotations that it can't handle. It isn't confused,
however, by embedded apostrophes and other common gotchas.

.. code-block:: pycon

    >>> words("don't be blue")
    ["don't", "be", "blue"]

    >>> words(""" "'this'" works '"great"' """)
    ["'this'", 'works', '"great"']

``words`` is a good choice for situations where you want a compact,
friendly, whitespace-delimited data representation--but a few of your
entries need more than just ``str.split()``.

Explicit Separators
-------------------

There is a second mode of operation for ``words`` in which
you provide explicit separators. This is handy if, for example,
you have a number of phrases with embedded spaces. This happens often
when importing data from spreadsheets.

.. code-block:: pycon

    >>> words('First Name / Last Name / Age / Best Feature', sep='/')
    ['First Name', Last Name', 'Age', 'Best Feature']

Here you have a very terse specification of the phrases, without
the need to quote in order to preserve embedded spaces.