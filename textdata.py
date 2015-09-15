"""
Conveniently get data from text
"""

import os
import re
from itertools import groupby
import sys
from io import StringIO

__all__ = 'lines text textlines textline words paras'.split()

_PY3 = sys.version_info[0] >= 3
if _PY3:
    basestring = str


CSTRIP = re.compile(r'#.*$', re.MULTILINE)  # comment stripping regex


def ensure_text(source):
    """
    Given either text or an interable, return the corresponding text. This
    common preprocess function allows ``textdata`` routines to take either
    text or an iterable, yet confidently process considering only the text
    case.
    """
    if isinstance(source, basestring):
        return source
    else:
        # a list, tuple, iterator, or generator giving lines of text;
        # convert to a single text for standard cleanups
        return "\n".join(list(source))


def lines(source, noblanks=True, dedent=True, lstrip=False, rstrip=True,
          cstrip=True, join=False):
    """
    Grab lines from a string. Discard initial and final lines if blank.

    :param str|lines source:  Text (or list of text lines) to be processed
    :param bool dedent:   a common prefix should be stripped from each line (default `True`)
    :param bool noblanks: allow no blank lines at all (default `True`)
    :param bool lstrip:   all left space be stripped from each line (default `False`);
                     dedent and lstrip are mutualy exclusive
    :param bool rstrip:   all right space be stripped from each line (default `True`)
    :param bool cstrip:   strips comment strings from # to end of each line (like Python itself)
    :param bool|str join:     if False, no effect; otherwise a string used to join the lines
    :return: a list of strings
    :rtype: list
    """

    text = ensure_text(source)

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

        # TODO: decided if these should be while loops, eating all prefix/suffix blank lines

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
        join = '' if join is True else join
        return join.join(textlines)


def text(source, **kwargs):
    """
    Like ``lines()``, but returns result as unified text. Useful primarily
    because of the nice cleanups ``lines()`` does.


    :param str|lines source:  Text (or list of text lines) to be processed
    :param str join: String to join lines with. Typically "\n" for line-oriented
        text but change to " " for a single continous line.
    :return: the cleaned string
    :rtype: str
    """
    kwargs.setdefault('join', '\n')
    return lines(source, **kwargs)


textlines = text


def textline(source, cstrip=True):
    """
    Like ``text()``, but returns result as unified string that is not
    line-oriented. Really a special case of ``text()``

    :param str|list source:
    :param bool cstrip: Should comments be stripped? (default: ``True``)
    :return: the cleaned string
    :rtype: str
    """
    pars = paras(source, keep_blanks=False, join=" ", cstrip=cstrip)
    return "\n\n".join(pars)


# define word regular expression and pre-define quotes
WORDRE = re.compile(r"""\s*(?P<word>"[^"]*"|'[^']*'|\S+)\s*""")
QUOTES = ("'", '"')


def noquotes(s):
    """
    Given a string ``s``, if it starts with a quote symbol,
    return the 'middle' part of the string with the quote symbol
    stripped off the ends.

    :param str s: Input string
    :return: String without quotes
    :rtype: str
    """
    if s.startswith(QUOTES) and s.endswith(QUOTES):
        return s.strip(s[0])
    else:
        return s


def words(source, cstrip=True):
    """
    Returns a series of words, somewhat like Like qw() in Perl. Similar to
    s.split(), except that it respects quoted spans (for the occasional
    'word' with spaces included.) Like ``lines``, removes comment strings by
    default.

    :param str|list source: Text (or list of text lines) to gather words from
    :param bool cstrip: Should comments be stripped? (default: ``True``)
    :return: list of words/phrases
    :rtype: list
    """

    text = ensure_text(source)

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
    separator (likely a newline if you want to preserve multi-line structure
    in the resulting string, or " " if you don't).  Like ``words``,
    ``lines``, and ``textlines``, will also strip comments by default.

    :param str|list source: Text (or list of text lines) from which paras are to be gathered
    :param keep_blanks: Should internal blank lines be retained (default: ``False``)
    :param bool|str join: Should paras be joined into a string? (default: ``False``).
    :param bool cstrip: Should comments be stripped? (default: ``True``)
    :return: list of strings (each a paragraph)
    :rtype: list
    """

    # make sure we have lines, with suitable cleanups
    # note that lines() will guarantee ensure_text()
    sourcelines = lines(source, noblanks=False, cstrip=cstrip)

    # get paragraphs
    results = []
    line_not_blank = lambda l: l.strip() != ""
    for non_blank, run in groupby(sourcelines, line_not_blank):
        if non_blank or keep_blanks:
            run_list = list(run)
            payload = join.join(run_list) if join is not False else run_list
            results.append(payload)
    return results
