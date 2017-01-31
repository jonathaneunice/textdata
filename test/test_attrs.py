
from textdata import *
from textdata.attrs import *
import sys
import pytest

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


def test_literal_eval():
    assert literal_eval('12') == 12
    assert literal_eval('1.5') == 1.5
    assert literal_eval('5j') == 5j
    assert literal_eval('this') == 'this'


def test_html_style_attrs():

    # should render attrs
    assert attrs('a=12 b=23') == { 'a': 12, 'b': 23 }
    assert attrs('a=12 b=23', literal=False) == { 'a': '12', 'b': '23' }

    # should render attrs with quotes
    assert attrs("""a="12" b='23' """) == { 'a': '12', 'b': '23' }
    assert attrs("""a="12" b='23' """, literal=False) == { 'a': '12', 'b': '23' }

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
    assert attrs('a:12 b:23', literal=False) == { 'a': '12', 'b': '23' }

    # should render attrs with : format separated with ;
    assert attrs('a:12; b:23') == { 'a': 12, 'b': 23 }
    assert attrs('a:12; b:23', literal=False) == { 'a': '12', 'b': '23' }

def test_partial_attrs():
    # should render partial attrs
    assert attrs('a="12" b=') == { 'a': '12', 'b': None }
    assert attrs('a')  == { 'a': None }
    assert attrs('a:') == { 'a': None }


def test_quoted_keys():
    assert attrs('"a"=this b=12') == { 'a': 'this', 'b': 12 }
    assert attrs('"a":this b:12') == { 'a': 'this', 'b': 12 }


def test_literal_or_not():

    # should not have problem with naked strings
    assert attrs('a=toast b:eggs c:9') == { 'a': 'toast', 'b': 'eggs', 'c': 9}

    # should render lteral attrs by default
    assert attrs('a=None') == { 'a': None }
    assert attrs('b=1.5') == { 'b': 1.5 }
    assert attrs('b=2e3') == { 'b': 2e3 }
    assert attrs('c=3j')  == { 'c': 3j }

    # or strings otherwise
    assert attrs('a=None', literal=False) == { 'a': 'None' }
    assert attrs('b=1.5', literal=False) == { 'b': '1.5' }
    assert attrs('b=2e3', literal=False) == { 'b': '2e3' }
    assert attrs('c=3j', literal=False)  == { 'c': '3j' }


@pytest.mark.skipif(_PYVER < (2,7),
                    reason="no OrderedDict type")
def test_astype():

    # astype should return a dict by default
    a = attrs('a=toast b:eggs c:9')
    assert a == { 'a': 'toast', 'b': 'eggs', 'c': 9}
    assert a == attrs('a=toast b:eggs c:9', astype=dict)
    assert isinstance(a, dict)

    # astype should return an OrderedDict if desired
    from collections import OrderedDict
    oa = attrs('a=toast b:eggs c:9', astype = OrderedDict)
    assert oa == a
    assert isinstance(oa, OrderedDict)
    assert list(oa.keys()) == ['a', 'b', 'c']
