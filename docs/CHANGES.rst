Change Log
==========

**2.4.1**  (January 23, 2019)

    Fixed error in ``table()`` parsing heuristic. Added tests. Tweaked
    docs.


**2.4.0**  (December 21, 2018)

    Added explicit separator mode to ``words()``.


**2.3.2**  (September 20, 2018)

    Removed ``print()`` inadvertently added in last release.


**2.3.0**  (September 15, 2018)

    Changed tab handling behavior. Previously used
    ``str.expandtabs()`` uniformly. While useful for dedent (removing
    common line indentation), could obscure important internal tabs.
    Default behavior is now to NOT expandtabs unless explicitly
    requested. However, leading tabs are still expanded for dedent
    processing.


**2.2.0**  (July 7, 2018)

    Reorganized code. Tidied and improved comments.

    Improved key cleaning for ``records()``

    Added ``full`` evaluation mode.

    Strengthened table evaluations.

    Improved tests and docs.

    Dropped deprecated ``astype`` and ``literal`` parameters to
    ``attrs()``.

    Drops support for Python 2.6. Mainstream support ended 5 years
    ago. Upgrade already!


**2.1.0**  (July 4, 2018)

    Removed debugging statement inadverntaently left in code.

    Improve documentation, esp. for APIs.

    Enable ``attrs``, ``table``, and ``records`` to take the same
    string or sequence of lines input as the outher routines.

    Cleaned up exported names. ``OrderedDict`` no longer exported as a
    convenience.


**2.0.2**  (July 3, 2018)

    Documentation tweaks.


**2.0.1** 

    Updated for new pypi.org URLs.

    Plus other minor tweaks, like tightening tox targets in favor of
    Travis CI.


**2.0.0**  (October 30, 2017)

    *Major* release.

    Added ``table()`` and ``records()`` functions for ingesting
    tabular and record-oriented data respectively.\

    Regularized handling of object evaluation, comment stripping, and
    other attributes.


**1.7.3**  (October 13, 2017)

    Added pyproject.toml for PEP 518 compliance.

    Updated testing matrix to accomodate new PyPy3 version on Travis
    CI.


**1.7.2**  (May 30, 2017)

    Update compatibility strategy to make Python 3 centric. Python 2
    is now the outlier. More future-proof.

    Doc tweaks.


**1.7.1**  (January 30, 2017)

    Returned test coverage to 100% of lines (introducing `attrs()`
    took it briefly down to 99% testing).


**1.7.0**  (January 30, 2017)

    Added `attrs()` function for parsing `dict` instances out of text.


**1.6.2**  (January 23, 2017)

    Updates testing. Newly qualified under 2.7.13 and 3.6, as well as
    most recent builds of pypy and pypy3.


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



