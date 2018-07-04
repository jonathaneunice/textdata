
import warnings

from .eval import evaluation
from .core import CSTRIP, ensure_text


# see something, say something
warnings.simplefilter('once', DeprecationWarning)


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
terminalChars = [' ', ';', ',', '\t', '\n']


def isQuote(s):
    return s in quoteChars


def attrs(source, 
          evaluate='natural', 
          dict=dict,
          cstrip=True,
          literal=True, 
          astype=None):
    """
    Parse attribute strings into a dict (or other mapping type).
    By default evaluates literals as natural to Python, e.g. turning
    what looks like numbers into into real ``int`` and ``float`` instances, 
    not just strings). 
    Quoted values are always treated as strings, never evaluated.

    Args:
        source (Union[str, List[str]]): Text to parse (as string or list of lines)
        evaluate (Union[str, bool]): How to evaluate resulting values
        dict (type): Type of mapping to return
        cstrip (bool): Remove comments from string before interpretation?
        astyle: Deprecated. Use ``dict`` parameter instead.
        literal: Deprecated. Use ``evaluate`` parameter instead.

    Returns:
        dict (or given dict type)
    """

    text = ensure_text(source)

    # deprecated API warnings and patchups
    if astype is not None:
        dict = astype
        msg = 'astype= parameter deprecated; use dict= instead'
        warnings.warn(msg, DeprecationWarning)
    if literal is not True:
        evaluate = 'minimal'
        msg = 'literal= parameter deprecated; use evaluate= instead'
        warnings.warn(msg, DeprecationWarning)

    # trim comments (optionally) and excess whitespace at ends
    if cstrip:
        text = CSTRIP.sub('', text).strip()
    text = text.strip()

    res = dict()
    tlen = len(text)
    cursor = 0

    # possible that cursor rests on terminator even to start
    while cursor < tlen and text[cursor] in terminalChars:
        cursor += 1

    # while still more data, tease it out
    while cursor < tlen:
        assignIndex = indexOfAny(text, equalsChars, cursor)
        if assignIndex is None:
            remaining = text[cursor:].strip()
            if remaining:
                res[remaining] = None
            return res

        left = text[cursor:assignIndex].strip()
        if left and isQuote(left[0]):
            left = left[1:-1]
        rcursor = assignIndex + 1
        # find the non-whitespace rhs of the attribute definition
        while rcursor < tlen and isWhitespace(text[rcursor]):
            rcursor += 1
        if rcursor >= tlen:
            res[left] = None
            return res
        elif isQuote(text[rcursor]):
            # find the end of quote as boundary of value
            endQuoteIndex = text.index(text[rcursor], rcursor+1)
            res[left] = text[rcursor + 1:endQuoteIndex]
            cursor = endQuoteIndex + 1
        else:
            # no quote value, ends with terminating whitespace or ; or ,
            endValueIndex = indexOfAny(text, [';', ',', ' ', '\t', '\n'], rcursor + 1);
            if endValueIndex is None:
                endValueIndex = tlen
            valueStr = text[rcursor:endValueIndex]
            res[left] = evaluation(valueStr, evaluate)
            cursor = endValueIndex + 1

        # possible that cursor still rests on terminator
        while cursor < tlen and text[cursor] in terminalChars:
            cursor += 1
    return res


class Dict(dict):
    """
    Attribute-accessible dict subclass. Does whatever a dict does, but its
    keys are also accessible via .attribute notation. Provided here as a
    convenience. Recommend you use `items.Item <https://pypi.org/project/items/>`_
    instead. It is more robust and complete.
    """
    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)
        self.__dict__ = self
    def __repr__(self):
        clsname = self.__class__.__name__
        inner = ', '.join('{0}={1!r}'.format(k,v) for k,v in self.items())
        return '{0}({1})'.format(clsname, inner)
