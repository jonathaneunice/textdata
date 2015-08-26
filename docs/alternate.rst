Alternate Data Paths
====================

``textdata`` is primarily designed to deal with text coming from source
code, but there's no reason it must be. Text coming from a file, from a
generator, or other sources can enjoy the module's text cleanups and
lightweight parsing.

To make this "from whatever source" ability more general, all of the
``textdata`` entry points (``lines``, ``textlines``, ``words``, and
``paras``) can accept a sequence of lines. Most often this will be a list of
lines, but it can also be an iterator, generator, or such that returns a
sequence of strings.

