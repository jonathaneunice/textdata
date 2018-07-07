# -*- coding: utf-8 -*-

import sys

import pytest
from textdata.eval import evaluation

_PY2 = sys.version_info[0] == 2
_PY26 = sys.version_info[:2] == (2, 6)


def test_evaluation_natural():
    cases = [
        ('  1  ', 1),
        ('  1.1  \n ', 1.1),
        (' gizmo \n\t \n', 'gizmo'),
    ]
    if not _PY26:
        cases.append((' 1+4j  ', 1+4j))
        # PY26 doesn't play nice with complex literals
        # Not worth fighting over.

    for value, expected in cases:
        assert evaluation(value) == expected
        assert evaluation(value.strip()) == expected
        assert evaluation(value, 'natural') == expected


def test_evaluation_none():
    cases = [
        ('  1  ', 1),
        ('  1.1  \n ', 1.1),
        (' gizmo \n\t \n', 'gizmo'),
        (' 1+4j  ', 1+4j)
    ]
    for value, _ in cases:
        assert evaluation(value, None) == value
        assert evaluation(value, 'none') == value


def test_evaluation_minimal():
    cases = [
        ('  1  ', '1'),
        ('  1.1  \n ', '1.1'),
        (' gizmo \n\t \n', 'gizmo'),
        (' 1+4j  ', '1+4j')
    ]
    for value, expected in cases:
        assert evaluation(value, 'minimal') == expected
        assert evaluation(value, False) == expected

def test_evaluation_broken():
    cases = [
        ('  1  ', '1'),
        ('  1.1  \n ', '1.1'),
        (' gizmo \n\t \n', 'gizmo'),
        (' 1+4j  ', '1+4j')
    ]
    for value, expected in cases:
        with pytest.raises(ValueError):
            assert evaluation(value, 'smork') == expected
        with pytest.raises(ValueError):
            assert evaluation(value, value) == expected


def test_py23_diff():
    if _PY2:
        assert evaluation('007', 'natural') == 7
    else:
        assert evaluation('007', 'natural') == '007'


def test_evaluation_func():
    custom = lambda x: x.strip().upper()
    def custom2(x):
        return x.strip().upper()
    assert evaluation('  haPpIly  ', custom) == 'HAPPILY'
    assert evaluation('  haPpIly  ', custom2) == 'HAPPILY'


def test_evaluation_full():
    cases = [
        ('  "1"  ', 1),
        ('  "1.1"  \n ', 1.1),
        (' gizmo \n\t \n', 'gizmo'),
        (' "gizmo" \n\t \n', 'gizmo'),
        (' "and space " \n\t \n', 'and space '),
        (' "a" ', 'a')
    ]
    if not _PY26:
        cases.append((' 1+4j  ', 1+4j))
        cases.append((' "1+4j"  ', 1+4j))
        # PY26 doesn't play nice with complex literals
        # Not worth fighting over.

    for value, expected in cases:
        assert evaluation(value.strip(), 'full') == expected


def test_evaluation_exception():
    def broken():
        raise ValueError
    assert evaluation(' mostly   ', broken) == 'mostly'
