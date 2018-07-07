
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

The ``table()`` function returns a list of lists, while the ``records()``
function uses the table header as keys and returns a list of dictionaries.

``table()`` and ``records()`` work even if you have a lot of extra fluff:

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
characters, plain text columns and borders, .... See the table tests for *dozens*
of samples of formats that work.

What constitutes table columns are contiguous bits of text, without intervening
whitespace. Typographic "rivers" of whitespace define column breaks. For this
reason, it's recommended that every table column have a separator line, usually
consistng of ``'-'``, ``'='``, or Unicode box drawing characters, to control
column width.

If there are ``'#'`` characters in your table data, best to pass
``cstrip=False`` so that they will not be erroneously interpreted as comments.

Records and Keys
----------------

Records depends on there being a header row available.

Many tables use natural language headers, such as ``First Name`` and ``Item Price``.
When retrieving records (dicts), this is not impossible, but it's often also not 
entirely convenient--especially for attribute-accessible dictionary keys. So ``records()``
provides a ``keyclean`` feature that passes each key through a cleanup function. 
By default whitespace at the start and end of the key are removed, multiple interior
whitespace characters are collapsed and replaced with underscore characters (`_`).

You can provide your own custom keyclean function if you like, or ``None`` if you
like your keys as-is.