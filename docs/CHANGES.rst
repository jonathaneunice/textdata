Change Log
==========

**1.6.1**  (September 15, 2015)

    Added Python 3.5.0 final and PyPy 2.6.1 to the testing matrix.


**1.6.0**  (September 1, 2015)

    Added ``textline()`` routine (NB ``textline`` not ``textlines``)
    as a quick "grab a single very long line" function.  It actually
    allows multiple paragraphs to be grabbed, each as a single long
    line, separated by double-newlines (i.e. Markdown style).


**1.5.0**  (September 1, 2015)

    Added ``text()`` as preferred synonym for ``textlines()``, as that
    is more consistent with the rest of the naming scheme. Deprecated
    ``textlines()``.


**1.4.3**  (August 26, 2015)

    Reorganizes documentation using Sphinx.


**1.4.2**  (August 17, 2015)

    Achieves 100% test coverage. Updated testing scheme to
    automatically evaluate and report combined coverage across
    multiple Python versions.


**1.4.0** 

    Allows all routines to accept a list of text lines, in addition to
    text as a single string.


**1.3.0** 

    Adds a paragraph constructor, ``paras``.


**1.2.0** 

    Adds comment stripping. Packaging and testing also tweaked.


**1.1.5** 

    Adds the ``bdist_wheel`` packaging format.


**1.1.3** 

    Switches from BSD to Apache License 2.0 and integrates ``tox``
    testing with ``setup.py``.


**1.1.0** 

    Added the ``words`` constructor.


**1.0** 

    Misc. changes from 1.0 or prior:

    Common line prefix is now computed without considering blank
    lines, so blank lines need not have any indentation on them just
    to "make things work."

    The tricky case where all lines have a common prefix, but it's not
    entirely composed of whitespace, now properly handled. This is
    useful for lines that are already "quoted" such as with leading
    ``"|"`` or ``">"`` symbols (common in Markdown and old-school
    email usage styles).

    ``textlines()`` is now somewhat superfluous, now that ``lines()``
    has a ``join`` kwarg.  But you may prefer it for the implicit
    indication that it's turning lines into text.



