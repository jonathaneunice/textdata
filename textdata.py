"""
Conveniently get data from text
"""

import os
import re
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

__all__ = 'lines textlines words'.split()

_PY3 = sys.version_info[0] >= 3
if _PY3:
    basestring = (str)


def lines(text, noblanks=True, dedent=True, lstrip=False, rstrip=True,
          join=False):
    """
    Grab lines from a string. First and last lines are assumed to be uninteresting if blank.
    :param text:     text to be processed
    :param dedent:   a common prefix should be stripped from each line (default `True`)
    :param noblanks: allow no blank lines at all (default `True`)
    :param lstrip:   all left space be stripped from each line (default `False`);
                     dedent and lstrip are mutualy exclusive
    :param rstrip:   all right space be stripped from each line (default `True`)
    :param join:     if False, no effect; otherwise a string used to join the lines
    """

    textlines = text.expandtabs().splitlines()

    # remove blank lines if noblanks
    if noblanks:
        textlines = [ line for line in textlines if line.strip() != '' ]
    else:
        # even if intermediate blank lines ok, first and last are due to Python formatting
        if textlines and textlines[0].strip() == "":
            textlines.pop(0)
        if textlines and textlines[-1].strip() == "":
            textlines.pop()

    if dedent and not lstrip:
        nonblanklines = [ line for line in textlines if line.strip() != "" ]
        prefix = os.path.commonprefix(nonblanklines)
        prelen, maxprelen = 0, len(prefix)
        while prelen < maxprelen and prefix[prelen] == ' ':
            prelen += 1
        if prelen:
            textlines = [ line[prelen:] for line in textlines ]

    # perform requested left and right space stripping (must be done
    # late so as to not interfere with dedent's common prefix detection)
    if lstrip and rstrip:
        textlines = [ line.strip() for line in textlines ]
    elif lstrip:
        textlines = [ line.lstrip() for line in textlines ]
    elif rstrip:
        textlines = [ line.rstrip() for line in textlines ]

    if join is False:
        return textlines
    else:
        if join is True:
            join = ''
        return join.join(textlines)


def textlines(text, **kwargs):
    """
    Like ``lines()``, but returns result as unified text. Useful primarily because
    of the nice cleanups ``lines()`` does.
    """
    kwargs.setdefault('join', '\n')
    return lines(text, **kwargs)


WORDRE = re.compile(r"""\s*(?P<word>"[^"]*"|'[^']*'|\S+)\s*""")
QUOTES = ("'", '"')

def noquotes(s):
    if s.startswith(QUOTES) and s.endswith(QUOTES):
        return s.strip(s[0])
    else:
        return s

def words(text):
    """
    Like qw() in Perl. Returns a series of words. Similar to
    s.split(), except that it respects quoted spans (for the
    occasional 'word' with spaces included.)
    """
    text = text.strip()
    parts = re.findall(WORDRE, text)
    return [noquotes(p) for p in parts]
