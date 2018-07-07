Attributes (Dicts)
==================

Dictionaries are hugely useful in Python, but not always the most compact to
state. In the literal form, key names must be quoted (unlike JavaScript),
and there are very specific key-value separation rules (using ``:`` in the
literal form, and ``=`` in the constructor form.

``textdata`` contains a more concise constructor, ``attrs``:

.. code-block:: pycon

    >>> attrs("a=1 b=2 c='something more'")
    {'a': 1, 'b': 2, 'c': 'something more'}

(The order in which key-value pairs appear may vary depending on what Python
verssion you're running. Python prior to 3.6 was almost perversly eager to
randomize dictionary order; see below for some workarounds.)

Note that:

1. Quotes are not required for keys; they're assumed to be strings.
2. No separators are required between key-value pairs (though commas and
   semicolons may be optionally used).
3. What would "natrually" be a numercial value in Python is indeed a
   numerical value, not the string representation you might assume a
   parsing routine would render.

Even better, colons may also be used as key-value separators, and
quotes are only required if the value includes spaces.

.. code-block:: pycon

    >>> attrs("a:1 b:2 c:'something more' d=sweet!")
    {'a': 1, 'b': 2, 'c': 'something more', d: 'sweet!'}

To make it easier to import from CSS,
semicolons may optionally be used to separate key-value pairs.

.. code-block:: pycon

    >>> attrs("a:1; b: green")
    {'a': 1, 'b': 'green'}

Finally, for familiarity with Python literal forms, keys may be quoted, and
key-value pairs may be separated by commas.

.. code-block:: pycon

    >>> attrs(" 'a': 1, 'the color': green")
    {'a': 1, 'the color': 'green'}

About the only option that isn't available is that keys are always interpreted
as strings, not lteral values, and the Python triple quote is not supported.

You might think that this level of flexibility would make parsing unreliable,
but it doesn't seem to be so. The ``attrs`` parser and its support code are
significantly tested. (And it's derived from a JavaScript codebase which is
itself significantly tested.) And supporting all these forms makes importing
content directly from from JavaScript, JSON, HTML, CSS, or XML quite
straightforward.

Evaluation
----------

``attrs`` tries hard to "do the right thing" with data presented to it,
including parsing the string form of numbers and other data types into natural
Python data types. However, that behavior is controllable. To disable the
parsing of Python literal values, set ``evaluate='minimal'`` (alternatively,
``evaluate=False``).

Evaluation behavior in general is configurable with the ``evaluate`` keyword
parameter. ``natural`` is the default, attempting to convert values that "look like"
``int``, ``float``, ``complex``, ``bool``, or ``None`` types into their corresponding 
Python values. 

The hard case is converting from HTML or XML, in which values are often quoted
regardless of intended type, so context is the only way to know if the type
should be textual or something else. Quotes are a very strong indicaton that
you want a string value type back. As a result, if you use quoted HTML/XML
forms, you have to specifically ask for ``full`` evaluation to get back numeric
and other value types.

.. code-block:: pycon

    >>> # Note values returned as strings, even though they look like numbers
    >>> # That's because they're explicitly quoted
    >>> attrs('a="1" b="2" c="something more"')
    {'a': '1', 'b': '2', 'c': 'something more'}

    >>> # Request 'full' evaluation to get numeric values 
    >>> attrs('a="1" b="2" c="something more"', evaluate='full')
    {'a': 1, 'b': 2, 'c': 'something more'}

Return Type
-----------

It's also a sad fact of Python life that, until version 3.6 (late 2016!), there
was no clean way to present a literal ``dict`` that would preserve the order of
keys in the same order as the source code. As a result, Python developers have
often needed the much less graceful ``collections.OrderedDict``, which, while
effective, lacked a clean literal form. ``attrs`` can help.:

.. code-block:: pycon

    >>> from collections import OrdredDict
    >>> attrs("a=1 b=2 c='something more'", dict=OrderedDict)
    OrderedDict([('a', 1), ('b', 2), ('c', 'something more')])

Terse, yet returns an ``OrderedDict`` with its keys in the expected order.

``attrs`` also exports ``Dict``, an attribute-accessible
``dict`` subclass. (Note, in future versions this will been
replaced with `items.Item <https://pypi.org/project/items/>`_,
an inherently ordered, attribute-accessible dictionary.

.. code-block:: pycon

    >>> attrs("a=1 b=2 c='something more'", dict=Dict)
    Dict(a=1, b=2, c='something more')

    >>> d = attrs("a=1 b=2 c='something more'", dict=Dict)
    >>> d.a
    1
    >>> d.a = 12
    >>> d
    Dict(a=12, b=2, c='something more')
