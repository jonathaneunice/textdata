Unicode and Encodings
=====================

.. |star| unicode:: 0x2605 .. star
    :trim:

``textdata`` doesn't have any unique friction with Unicode
characters and encodings. That said, any time you use Unicode characters
in Python source files, care is warranted--especially in Python 2!

If your text includes Unicode, in Python 2 make sure to
mark literal strings with a "u" prefix: ``u"`` |star| ``"``. You can
also do this in Python 3.3 and following. Sadly, there was a dropout
of compatibility in early Python 3 releases, making it much harder to
maintain a unified source base with them in the mix. (A
compatibility function such as ``six.u`` from
`six <http://pypi.python.org/pypi/six>`_
can help alleviate much--though certainly not all--of the pain.)

It can also be helpful to declare your source encoding: put
a specially-formatted comment as the first or second line of the source code:

    # -*- coding: <encoding name> -*-

This will usually be ``# -*- coding: utf-8 -*-``, but other encodings are
possible. Python 3 defaults to a UTF-8 encoding, but Python 2 assumes
ASCII.

