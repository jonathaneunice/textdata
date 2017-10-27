
import warnings
try:
    from collections import OrderedDict
except ImportError:
    pass
from .eval import evaluation


# see something, say something
warnings.simplefilter('always', DeprecationWarning)


def indexOfAny(s, sub, start=None, end=None):
    """
    Like `str.find`, except instead of a single sub, accepts
    a list of subs. Returns the minimum index of all such
    subs, or `None` if none exists. Search can be constrained to
    given start and end values.
    """
    indices = [ s.find(sv, start, end) for sv in sub ]
    try:
        return min(i for i in indices if i >= 0)
    except ValueError:
        return None


def isWhitespace(s):
    return s.strip() == ''


quoteChars  = ["'", '"']
equalsChars = ['=', ':']


def isQuote(s):
    return s in quoteChars


def attrs(s, evaluate='natural', dict=dict,
          literal=True, astype=None):
    """
    Parse attribute strings into a dict, which is returned. Optionally
    (and by default) evaluate literals (e.g. turn numbers into real
    int and float instances, not just strings of same). Quoted values
    are always strings, never evaluated.

    Unquoted: x=1 y=3
    Quoted:  x="1 and 2" y='3'

    Partial: x=
    Partial: x
    CSS style: x: 1; y: 3
    CSS style quoted: x: "1 and 2"; y: '3'
    """
    if astype is not None:
        dict = astype
        msg = 'astype= parameter deprecated; use dict= instead'
        warnings.warn(msg, DeprecationWarning)
    if literal is not True:
        evaluate = 'minimal'
        msg = 'literal= parameter deprecated; use evaluate= instead'
        warnings.warn(msg, DeprecationWarning)

    s = s.strip()
    res = dict()
    slen = len(s)
    cursor = 0

    while cursor < slen:
        assignIndex = indexOfAny(s, equalsChars, cursor)
        if assignIndex is None:
            remaining = s[cursor:].strip()
            if remaining:
                res[remaining] = None
            return res

        left = s[cursor:assignIndex].strip()
        if left and isQuote(left[0]):
            left = left[1:-1]
        rcursor = assignIndex + 1
        # find the non-whitespace rhs of the attribute definition
        while rcursor < slen and isWhitespace(s[rcursor]):
            rcursor += 1
        if rcursor >= slen:
            res[left] = None
            return res
        elif isQuote(s[rcursor]):
            # find the end of quote as boundary of value
            endQuoteIndex = s.index(s[rcursor], rcursor+1)
            res[left] = s[rcursor + 1:endQuoteIndex]
            cursor = endQuoteIndex + 1
        else:
            # no quote value, ends with whitespace or ; or ,
            endValueIndex = indexOfAny(s, [';', ',', ' ', '\t', '\n'], rcursor + 1);
            if endValueIndex is None:
                endValueIndex = slen
            valueStr = s[rcursor:endValueIndex]
            res[left] = evaluation(valueStr, evaluate)
            cursor = endValueIndex + 1
    return res


class Dict(dict):
    """
    Attribute-accessible dict subclass. Does whatever a dict does, but its
    keys are also accessible via .attribute notation. Provided here as a
    convenience.
    """
    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)
        self.__dict__ = self
    def __repr__(self):
        clsname = self.__class__.__name__
        inner = ', '.join('{0}={1!r}'.format(k,v) for k,v in self.items())
        return '{0}({1})'.format(clsname, inner)
