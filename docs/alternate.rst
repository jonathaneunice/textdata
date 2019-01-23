Alternate Data Paths
====================

``textdata`` is primarily designed to deal with data embedded into source code,
but there's no reason text coming from a file, a generator, or other sources
can't enjoy the module's text cleanups and lightweight parsing.

To make this "from whatever source" ability more general, all the main
``textdata`` entry points (``lines``, ``text``, ``words``, ``paras``,
``table``, and ``records``) can accept either a unified string or a sequence of
text lines. Most often this will be a list of strings (one per line), but it
can also be an iterator, generator, or such that returns a sequence of strings.
