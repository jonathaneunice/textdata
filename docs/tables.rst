
Tables
======

Much data comes in tabular format. The ``table()`` and ``records()``
functions help you extract it in convenient ways...either as a list
of lists, or as a list of dictionaries.

.. code-block:: pycon

    >>> text = """
    ...     name  age  strengths
    ...     ----  ---  ---------------
    ...     Joe   12   woodworking
    ...     Jill  12   slingshot
    ...     Meg   13   snark, snapchat
    ... """

    >>> table(text)
    [['name', 'age', 'strengths'],
     ['Joe', 12, 'woodworking'],
     ['Jill', 12, 'slingshot'],
     ['Meg', 13, 'snark, snapchat']]

    >>> records(text)
    [{'name': 'Joe', 'age': 12, 'strengths': 'woodworking'},
     {'name': 'Jill', 'age': 12, 'strengths': 'slingshot'},
     {'name': 'Meg', 'age': 13, 'strengths': 'snark, snapchat'}]

Note that ``table()`` works even if you have a table with a lot of extra fluff:

.. code-block:: pycon

    >>> fancy = """
    ... +------+-----+-----------------+
    ... | name | age | strengths       |
    ... +------+-----+-----------------+
    ... | Joe  |  12 | woodworking     |
    ... | Jill |  12 | slingshot       |
    ... | Meg  |  13 | snark, snapchat |
    ... +------+-----+-----------------+
    ... """
    >>> assert table(text) == table(fancy)
    >>> assert records(text) == records(fancy)

The parsing algorithm is heuristic, but works well with tables formatted in a
variety of conventional ways including Markdown, RST, ANSI/Unicode line drawing
characters, plain text columns and borders, .... See the table tests for dozens
of samples of formats that work.

What constitutes table columns are contiguous bits of text, without intervening
whitespace. Typographic "rivers" of whitespace define column breaks. For this
reason, it's recommended that every table column have a separator line, usually
consistng of ``'-'``, ``'='``, or Unicode box drawing characters, to control
column width.

If there are ``'#'`` characters in your table data, best to pass
``cstrip=False`` so that they will not be erroneously interpreted as comments.
