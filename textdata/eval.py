"""
Common support functions for evaluating values into
natural Python values, or possibly custom post-processing.
"""

from ast import literal_eval as ast_literal_eval


def literal_eval(s):
    """
    Wrapper around ``ast.literal_eval`` that returns its return value,
    if possible, but returns the original string in cases where
    ``ast.literal_eval`` raises an exception.
    """
    try:
        return ast_literal_eval(s)
    except (ValueError, SyntaxError):
        return s


EVALUATE = {
    None:      lambda s: s,
    'none':    lambda s: s,
    'minimal': lambda s: s.strip(),
    False:     lambda s: s.strip(),
    'natural': lambda s: literal_eval(s.strip()),
}


def evaluation(value, how='natural'):
    """
    Standard value evaluator. Defaults to the "natural"
    Python literal encoding.
    """
    if hasattr(how, '__call__'):
        return how(value)
    return EVALUATE[how](value)
