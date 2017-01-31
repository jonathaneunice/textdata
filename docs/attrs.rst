Attributes (Dicts)
==================

Dictionaries are hugely useful in Python, but not always the most
compact to state. In the literal form, key names have to be quoted
(unlike JavaScript), and there are very specific key-value separation
rules (using ``:`` in the literal form, and ``=`` in the constructor
form.

``textdata`` contains a more concise constructor, ``attrs``:

    >>> attrs("a=1 b=2 c='something more'")
    {'a': 1, 'c': 'something more', 'b': 2}

Note that quotes are not required for keys, there are no required
separators between key-value pairs, and that the values for numercial
values are rendered from string representation into
actual Python ``int`` (or ``float``, ``complex``, etc.) types. Pretty
slick, huh?

Even better, colons may also be used as key-value separators, and
quotes are only required if the value includes spaces.:

    >>> attrs("a:1 b:2 c:'something more'")
    {'a': 1, 'b': 2, 'c': 'something more'}

This makes specifying dictionary contents easier and less verbose, and
makes it easier to import from JavaScript, HTML, or XML.
To make it easier to import from CSS, semicolons may be used to separate
key-value pairs.:

    >>> attrs("a:1; b: green")
    {'a': 1, 'b': 'green'}

Finally, for familiarity with Python literal forms, keys may be
quoted, and key-value pairs may
be separated by commas.:

    >>> attrs(" 'a':1, 'the color': green")
    {'a': 1, 'the color': 'green'}

About the only option that isn't available is that keys are always strings,
not lteral values, and the Python triple quote is not supported.

You might think that this level of generality and flexibility would make
parsing unreliable, but it doesn't seem to be so. The ``attrs`` parser and
its support code are significantly tested.

Literals and Return Type
------------------------

``attrs`` tries hard to "do the right thing" with data presented to it,
iincluding parsing the string form of numbers and other data types into those
data types. However, that behavior is controllable. To disable the parsing of
Python literal values, set ``literal=False``.

It's also a sad fact of Python life that, until version 3.6 (late 2016!),
there was no clean way to present a literal ``dict`` that would preserve
the order of keys in the same order as the source code. As a result,
we've had to use the much less graceful ``collections.OrderedDict``, which,
while effective, lacked a clean literal form. ``attrs`` can help. On Python
versions prior to 3.6, try:

    from collections import OrderedDict
    
    attrs('a=1 b=2 c=3', astype=OrderedDict)

Which is terse, yet returns an ``OrderedDict`` with its
keys in the expected order.
