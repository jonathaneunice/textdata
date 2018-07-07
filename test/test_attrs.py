
import sys
from numbers import Number

import pytest

from textdata import *
from textdata.attrs import *

_PYVER = sys.version_info[:3]


def test_isQuote():

    # should accept single quotes
    assert isQuote("'")

    # should accept double quotes
    assert isQuote('"')

    # should not recognize other characters
    nonQuotes = list("!@#$$%^&*()abcdeABCDE_")
    for c in list("!@#$$%^&*()abcdeABCDE_"):
        assert not isQuote(c)


def test_isWhitespace():

    # should accept spaces
    assert isWhitespace("  ")

    # should accept tabs
    assert isWhitespace("\t")

    # should accept newlines
    assert isWhitespace("\n")

    # should not recognize other characters
    for c in list("!@#$$%^&*()abcdeABCDE_"):
        assert not isWhitespace(c)


def test_indexOfAny():

    # should find appropriate sub-strings
    assert indexOfAny('this=that', ['=', ':']) == 4
    assert indexOfAny('this:that', ['*', ':']) == 4

    # should return None if not found
    assert indexOfAny('this-that', ['=', ':']) is None
    assert indexOfAny('this/that', ['*', ':']) is None


def test_html_style_attrs():

    # should render attrs
    assert attrs('a=12 b=23') == { 'a': 12, 'b': 23 }
    assert attrs('a=12 b=23', evaluate='minimal') == { 'a': '12', 'b': '23' }


    # should render attrs with quotes
    assert attrs("""a="12" b='23' """) == { 'a': '12', 'b': '23' }
    assert attrs("""a="12" b='23' """, evaluate='minimal') == { 'a': '12', 'b': '23' }
    assert attrs("""a="12" b='23' """, evaluate='natural') == { 'a': '12', 'b': '23' }
    assert attrs("""a="12" b='23' """, evaluate='full') == { 'a': 12, 'b': 23 }


    # should render attrs with spaces in quotes
    assert attrs("""a="12 to 13" b='23 or more'""") == \
                     { 'a': '12 to 13', 'b': '23 or more' }


def test_css_style_attrs():
    # should render css attrs with quotes
    assert attrs("""a: "12" b: '23'""") == { 'a': '12', 'b': '23' }

    # should render css attrs with spaces in quotes
    assert attrs("""a: "12 to 13" b:'23 or more'""") == \
                     { 'a': '12 to 13', 'b': '23 or more' }

    # should render attrs with : format
    assert attrs('a:12 b:23') == { 'a': 12, 'b': 23 }
    assert attrs('a:12 b:23', evaluate='minimal') == { 'a': '12', 'b': '23' }

    # should render attrs with : format separated with ;
    assert attrs('a:12; b:23') == { 'a': 12, 'b': 23 }
    assert attrs('a:12; b:23', evaluate='minimal') == { 'a': '12', 'b': '23' }


def test_partial_attrs():
    # should render partial attrs
    assert attrs('a="12" b=') == { 'a': '12', 'b': None }
    assert attrs('a')  == { 'a': None }
    assert attrs('a:') == { 'a': None }


def test_attr_cstrip():
    t1 = """ a=1 b="two" # a comment """
    assert attrs(t1) == {'a': 1, 'b': 'two'}
    assert attrs(t1) == attrs(t1, cstrip=True)
    t2 = """
        a:1
        b: "# not a comment"
    """
    assert attrs(t2, cstrip=False) == {'a': 1, 'b': '# not a comment'}


def test_quoted_keys():
    assert attrs('"a"=this b=12') == { 'a': 'this', 'b': 12 }
    assert attrs('"a":this b:12') == { 'a': 'this', 'b': 12 }


def construct_spec(keys, values, quote, equals, terminal):

    quoteChars  = [None, "'", '"']
    terminalChars = [' ', ',', ';']
    pieces = []
    for key, value in zip(keys, values):
        if isinstance(value, Number):
            value_str = str(value)
        else:
            if isinstance(value, str):
                if quote is None:
                    # check if needs overriding
                    if indexOfAny(value, terminalChars) >= 0 and quote is None:
                        quote = "'"
                    else:
                        qi = indexOfAny(quoteChars[1:])
                        if qi >= 0:
                            quote = "'" if value[qi] == '"' else '"'
            value_str = str(value) if quote is None else '{0}{1}{0}'.format(quote, value)
        piece = '{0}{1}{2}'.format(key, equals, value_str)
        pieces.append(piece)
    return terminal.join(pieces)


def test_mixed_syntax():
    spec = "a:1 b:2 c:'something more' d=sweet!"
    expected = {'a': 1, 'b': 2, 'c': 'something more', 'd': 'sweet!'}
    # from docs
    assert attrs(spec) == expected

    keys = list('abcd')
    values = [1, 2, 'something more', 'sweet!']
    quoteValues  = [None, "'", '"']
    equalsValues = ['=', ':']
    terminalValues = [' ', '  ', ',', ', ', ';', '; ']
    for quote in quoteValues:
        for equals in equalsValues:
            for terminal in terminalValues:
                spec = construct_spec(keys, values, quote, equals, terminal)
                result = attrs(spec)
                assert result == expected

    # TODO: randomized testing of inter-mixed parameters


def test_perverse_terminators():
    # other tests broader but this one targets perverse/difficult cases
    # that have either caused problems in the past, or are imagined could do so
    expected = {'a': 1, 'b': 2, 'c': 'something more', 'd': 'sweet!'}

    # quote then terminator
    spec = "a:1 b:2 c:'something more', d=sweet!"
    result = attrs(spec)
    assert result == expected

    # multiple or empty terminators
    spec = "a:1 b:2,, c:'something more', d=sweet!"
    result = attrs(spec)
    assert result == expected

    # many empty terminators
    spec = "a:1 b:2,, ;   ; c:'something more';, ; d=sweet!;,  \n;"
    result = attrs(spec)
    assert result == expected

    # terminators before start
    spec = ",;; a:1 b:2,, ;   ; c:'something more';, ; d=sweet!;,  \n;"
    result = attrs(spec)
    assert result == expected


def test_literal_or_not():

    # should not have problem with naked strings
    assert attrs('a=toast b:eggs c:9') == { 'a': 'toast', 'b': 'eggs', 'c': 9}

    # should render lteral attrs by default
    assert attrs('a=None') == { 'a': None }
    assert attrs('b=1.5') == { 'b': 1.5 }
    assert attrs('b=2e3') == { 'b': 2e3 }
    assert attrs('c=3j')  == { 'c': 3j }

    # or strings otherwise
    assert attrs('a=None', evaluate='minimal') == { 'a': 'None' }
    assert attrs('b=1.5', evaluate='minimal') == { 'b': '1.5' }
    assert attrs('b=2e3', evaluate='minimal') == { 'b': '2e3' }
    assert attrs('c=3j', evaluate='minimal')  == { 'c': '3j' }


def test_explicit_dict_type():

    a = attrs('a=toast b:eggs c:9')
    assert a == { 'a': 'toast', 'b': 'eggs', 'c': 9}
    assert a == attrs('a=toast b:eggs c:9', dict=dict)
    assert isinstance(a, dict)

    from collections import OrderedDict
    oa = attrs('a=toast b:eggs c:9', dict=OrderedDict)
    assert oa == a
    assert isinstance(oa, OrderedDict)
    assert list(oa.keys()) == ['a', 'b', 'c']

    d = attrs('a=toast b:eggs c:9', dict=Dict)
    assert d == a
    assert isinstance(d, Dict)
    assert set(d.keys()) == set(['a', 'b', 'c'])


def test_docs():
    """Test examples from the docs"""

    # JavaScript
    assert attrs("a: 1, b: 2, c: 'something more'") == {'a': 1, 'b': 2, 'c': 'something more'}

    # JSON
    assert attrs('"a": 1, "b": 2, "c": "something more"') == {'a': 1, 'b': 2, 'c': 'something more'}

    # HTML or XML
    assert attrs('a="1" b="2" c="something more"') == {'a': '1', 'b': '2', 'c': 'something more'}

    # 'full' evaluation needed to transform strings into values
    assert attrs('a="1" b="2" c="something more"', evaluate='full') == {'a': 1, 'b': 2, 'c': 'something more'}

    # CSS
    assert attrs("a: 1; b: 2; c: 'something more'") == {'a': 1, 'b': 2, 'c': 'something more'}


def test_unclosed_quote():
    with pytest.raises(ValueError):
        attrs("a: 1, b: 2, c: 'something more")


def test_Dict():
    D = Dict(a=1, b=12, c=100.1, msg='Hello')
    d = {'a': 1, 'b': 12, 'c': 100.1, 'msg': 'Hello'}

    assert D == d
    for key in d.keys():
        assert D[key] == d[key]
        assert getattr(D, key) == d[key]


    D2 = Dict(one=1, two='too')
    D2_repr = repr(D2)

    assert D2_repr in ["Dict(one=1, two='too')",
                       "Dict(two='too', one=1)"]
