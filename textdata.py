"""
Conveniently get data from text
"""

import os
import re
from itertools import groupby
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

__all__ = 'lines textlines words paras'.split()

_PY3 = sys.version_info[0] >= 3
if _PY3:
    basestring = str

import re

CSTRIP = re.compile(r'#.*$', re.MULTILINE)


def lines(text, noblanks=True, dedent=True, lstrip=False, rstrip=True,
          cstrip=True, join=False):
    """
    Grab lines from a string. First and last lines are assumed to be uninteresting if blank.
    :param text:     text to be processed
    :param dedent:   a common prefix should be stripped from each line (default `True`)
    :param noblanks: allow no blank lines at all (default `True`)
    :param lstrip:   all left space be stripped from each line (default `False`);
                     dedent and lstrip are mutualy exclusive
    :param rstrip:   all right space be stripped from each line (default `True`)
    :param cstrip:   strips comment strings from # to end of each line (like Python itself)
    :param join:     if False, no effect; otherwise a string used to join the lines
    """

    if cstrip:
        text = CSTRIP.sub('', text)

    textlines = text.expandtabs().splitlines()

    # remove blank lines if noblanks
    if noblanks:
        textlines = [line for line in textlines if line.strip() != '']
    else:
        # even if intermediate blank lines ok, first and last are due to Python
        # formatting
        if textlines and textlines[0].strip() == "":
            textlines.pop(0)
        if textlines and textlines[-1].strip() == "":
            textlines.pop()

    if dedent and not lstrip:
        nonblanklines = [line for line in textlines if line.strip() != ""]
        prefix = os.path.commonprefix(nonblanklines)
        prelen, maxprelen = 0, len(prefix)
        while prelen < maxprelen and prefix[prelen] == ' ':
            prelen += 1
        if prelen:
            textlines = [line[prelen:] for line in textlines]

    # perform requested left and right space stripping (must be done
    # late so as to not interfere with dedent's common prefix detection)
    if lstrip and rstrip:
        textlines = [line.strip() for line in textlines]
    elif lstrip:
        textlines = [line.lstrip() for line in textlines]
    elif rstrip:
        textlines = [line.rstrip() for line in textlines]

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


def words(text, cstrip=True):
    """
    Like qw() in Perl. Returns a series of words. Similar to
    s.split(), except that it respects quoted spans (for the
    occasional 'word' with spaces included.) Like ``lines``,
    removes comment strings by default.
    """

    if cstrip:
        text = CSTRIP.sub('', text)

    text = text.strip()
    parts = re.findall(WORDRE, text)
    return [noquotes(p) for p in parts]


def paras(source, keep_blanks=False, join=False, cstrip=True):
    """
    Given a string or list of text lines, return a list of lists where each
    sub list is a paragraph (list of non-blank lines). If the source is a
    string, use ``lines`` to split into lines. Optionally can also keep the
    runs of blanks, and/or join the lines in each paragraph with a desired
    separator (likely "\n" if you want to preserve multi-line structure
    in the resulting string, or " " if you don't).  Like ``words``,
    ``lines``, and ``textlines``, will also strip comments by default.
    """

    # make sure we have lines
    if isinstance(source, basestring):
        sourcelines = lines(source, noblanks=False, cstrip=cstrip)
    else:
        if cstrip:
            source = [ CSTRIP.sub('', line) for line in source ]
        # TODO: should lines() take a list of lines just pass the lines through it?
        sourcelines = source

    # get paragraphs
    results = []
    line_not_blank = lambda l: l.strip() != ""
    for non_blank, run in groupby(sourcelines, line_not_blank):
        if non_blank or keep_blanks:
            run_list = list(run)
            payload = join.join(run_list) if join is not False else run_list
            results.append(payload)
    return results
