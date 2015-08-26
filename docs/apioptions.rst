Lines and Textlines
===================

Both ``lines`` and ``textlines`` provide provide routinely-needed cleanups:

  * remove starting and ending blank lines
    (which are usually due to Python source formatting)
  * remove blank lines internal to your text block
  * remove common indentation
  * strip leading/trailing spaces other than the common prefix
    (leading spaces removed by request, trailing by default)
  * strip any comments from the end of lines
  * join lines together with your choice of separator string


``lines(source, noblanks=True, dedent=True, lstrip=False, rstrip=True, cstrip=True, join=False)``

    Returns text as a series of cleaned-up lines.

    * ``source`` is the text to be processed.
    * ``noblanks`` => all blank lines are eliminated, not just starting and ending ones. (default ``True``).
    * ``dedent`` => strip a common prefix (usually whitespace) from each line (default ``True``).
    * ``lstrip`` => strip all left (leading) space from each line (default ``False``).
      Note that ``lstrip`` and ``dedent`` are  mutually exclusive ways of handling leading space.
    * ``rstrip`` => strip all right (trailing) space from each line (default ``True``)
    * ``cstrip`` => strip comments (from ``#`` to the end of each line (default ``True``)
    * ``join`` => either ``False`` (do nothing), ``True`` (concatenate lines with ``\n``),
      or a string that will be used to join the resulting lines (default ``False``)

``textlines(source, noblanks=True, dedent=True, lstrip=False, rstrip=True, cstrip=True, join='\n')``

    Does the same helpful cleanups as ``lines()``, but returns
    result as a single string, with lines separated by newlines (by
    default) and without a trailing newline.

.. note:: Text cleanups inherently convert tabs to sequences of spaces,
    consistent with Python's ``str.expandtabs``. There is currently no option
    to turn this behavior off.

