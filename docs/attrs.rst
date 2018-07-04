Attributes (Dicts)
==================

Dictionaries are hugely useful in Python, but not always the most
compact to state. In the literal form, key names have to be quoted
(unlike JavaScript), and there are very specific key-value separation
rules (using ``:`` in the literal form, and ``=`` in the constructor
form.

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
   semicolons may be optionally used; more on this in a minute).
3. What would "natrually" be a numercial value in Python is indeed a
   numerical value, not the string representation you might assume a
   parsing routine would render.

Even better, colons may also be used as key-value separators, and
quotes are only required if the value includes spaces.::

.. code-block:: pycon

    >>> attrs("a:1 b:2 c:'something more' d=sweet!")
    {'a': 1, 'b': 2, 'c': 'something more', d: 'sweet!'}

That may seem overkill, but it makes it much easier to directly import content
from JavaScript, HTML, CSS, or XML. To make it easier to import from CSS,
semicolons may optionall be used to separate key-value pairs.:

.. code-block:: pycon

    >>> attrs("a:1; b: green")
    {'a': 1, 'b': 'green'}

Finally, for familiarity with Python literal forms, keys may be
quoted, and key-value pairs may
be separated by commas.:

.. code-block:: pycon

    >>> attrs(" 'a':1, 'the color': green")
    {'a': 1, 'the color': 'green'}

About the only option that isn't available is that keys are always strings,
not lteral values, and the Python triple quote is not supported.

You might think that this level of flexibility would make
parsing unreliable, but it doesn't seem to be so. The ``attrs`` parser and
its support code are significantly tested. (And it's derived from a
JavaScript codebase which is itself significantly tested.)

Literals
--------

``attrs`` tries hard to "do the right thing" with data presented to it,
iincluding parsing the string form of numbers and other data types into
natual Python
data types. However, that behavior is controllable. To disable the parsing of
Python literal values, set ``literal=False``.

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

Which is terse, yet returns an ``OrderedDict`` with its
keys in the expected order. 

``attrs`` also exports ``Dict``, an attribute-accessible
dictionary subclass. (Note, in future versions this will been
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


Deprecations
------------

Previous versions of ``attrs`` supported keyword options ``literal`` to turn
on/off interpretation into Python values, and ``astype`` to control the type of
the dictionary returned. Those options have been superceeded by ``evaluate``
(set ``evaluate='natural'`` for the old ``literal=True`` or
``evaluate='minimal'`` or ``evaluate=False``) for the old ``literal=False``).
``dict`` for ``astype`` is just a name change.
