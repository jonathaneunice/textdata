Paragraphs
==========

Sometimes you want to collect "paragraphs"--contiguous runs of text lines
delineated by blank lines. Markdown and RST document formats,
for example, use this convention.

.. code-block:: pycon

    >>> rhyme = """
        Hey diddle diddle,

        The cat and the fiddle,
        The cow jumped over the moon.
        The little dog laughed,
        To see such sport,

        And the dish ran away with the spoon.
    """
    >>> paras(rhyme)
    [['Hey diddle diddle,'],
     ['The cat and the fiddle,',
      'The cow jumped over the moon.',
      'The little dog laughed,',
      'To see such sport,'],
     ['And the dish ran away with the spoon.']]

Or if you'd like each paragraph in a single string:

.. code-block:: pycon

    >>> paras(rhyme, join="\n")
    ['Hey diddle diddle,',
     'The cat and the fiddle,\nThe cow jumped over the moon.\nThe little dog laughed,\nTo see such sport,',
     'And the dish ran away with the spoon.']

Setting ``join`` to a space will of course concatenate the lines of each
paragraph with a space. This can be useful for converting from line-oriented
paragraphs into each-paragraph as a (potentially very long) single line, a
format useful for cut-and-pasting into many editors and text entry boxes on the
Web, or for email systems.

On the off chance you want to preserve the exact intra-paragraph spacing,
setting ``keep_blanks=True`` will accomplish that.
