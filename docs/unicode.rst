Unicode and Encodings
=====================

.. |star| unicode:: 0x2605 .. star
    :trim:

``textdata`` doesn't have any unique friction with Unicode characters and
encodings. That said, any time you use Unicode characters in Python 2 source
files, care is warranted.

Best advice is: It's time to upgrade already! Python 3 is lovely and
ever-improving. Python 2 is now showing its age.

If you do need to continue supporting Python 2, either make sure your literal
strings are marked with a "u" prefix: ``u"`` |star| ``"``. To turn Unicode
literal processing on by default.

.. code-block: python

    from __future__ import unicode_literals

    # or better yet:
    # from __future__ import unicode_literals, print_function, division

You can explicitly mark strings as unicode in Python 3.3 and following,
though it's only necessary if you're maintaing backwards portability,
since Python 3 strings are by default Unicode strings.

It can also be helpful (amd in Python 2, often strictly necessary)
to declare your source encoding by putting a specially-formatted
`PEP 263 <https://www.python.org/dev/peps/pep-0263/>`_
comment as the first or second line of the source code:

.. code-block:: python

    # -*- coding: utf-8 -*-

This will usually endorse UTF-8, but other encodings are possible. Python 3
defaults to a UTF-8 encoding, but Python 2 sadly assumes ASCII.

Finally, if you are reading from or writing to a file on Python 2,
strongly recommend you use an alternate form of ``open`` that
supports automatic encoding (which is built-in to Python 3). E.g.::

    from codecs import open

    with open('filepath', encoding='utf-8') as f:
        data = f.read()

This construction works across Python 2 and 3. Just add a ``mode='w'`` for
writing.
