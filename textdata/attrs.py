
from ast import literal_eval as ast_literal_eval

def indexOfAny(s, sub, start=None, end=None):
    """
    Like s`tr.find`, except instead of a single sub, accepts
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

def literal_eval(s):
    """
    Wrapper around ``ast.literal_eval`` that returns its return value,
    if possible, but returns the original string in cases where
    ``ast.literal_eval`` raises an exception.
    """
    try:
        return ast_literal_eval(s)
    except ValueError:
        return s

def attrs(s, literal=True, astype=dict):
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
    s = s.strip()
    res = astype()
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
            res[left] = literal_eval(valueStr) if literal else valueStr
            cursor = endValueIndex + 1
    return res
