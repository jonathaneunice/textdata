
import re
import sys

_PY2 = sys.version_info[0] == 2
if not _PY2:
    basestring = str

CSTRIP = re.compile(r'#.*$', re.MULTILINE)  # comment stripping regex


def ensure_text(source):
    """
    Given either text or an iterable, return the corresponding text. This
    common pre-process function allows ``textdata`` routines to take either
    text or an iterable, yet confidently process considering only the text
    case.
    """
    if isinstance(source, basestring):
        return source
    else:
        # a list, tuple, iterator, or generator giving lines of text;
        # convert to a single text for standard cleanups
        return "\n".join(list(source))


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