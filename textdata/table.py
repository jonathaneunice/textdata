# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals
import re
from intspan import intspan
import textwrap
from pprint import pprint

try:
    basestring
    # Python 2
except NameError:
    # Python 3
    basestring = str

from .eval import evaluation
from .core import CSTRIP

"""
Cases:

1. Bordered table with explicit column vertical separators. Read positions
   of separators, use those.
2. Some separator, but no (or insufficient) vertical indicators. Use the
   indicators given, but also use rivers.
3. No separators. Use rivers exclusively. Current code focused on this
   approach, but gave ability to provide an explicit colguide

Need to evaluate whether some separators span the entire table,
and so should not be used for finding spaces. In those cases, maybe
use shortest separator line?

"""


def all_indices(s, substr):
    """
    Find all indices in s where substr begins.
    Returns results in list.
    """
    indices = []
    i = s.find(substr)
    while i >= 0:
        indices.append(i)
        i = s.find(substr, i+1)
    return indices


def is_separator(line):
    """
    Does the given line consist solely of separator characters?
    -=+: and Unicode line-drawing equivalents
    """
    return bool(re.match(r"^[-=+:|\.`'\s\u2500-\u257F]*$", line))


def vertical_sep_in_line(line):
    """
    Find the indices in a line which are potentially to probably
    vertical separators.
    """
    VERTICAL_SEP = r"[+|\.`'╔╦╗╠╬╣╚╩╝┌┬┐╞╪╡├┼┤└┴┘]"
    return [m.start() for m in re.finditer(VERTICAL_SEP, line)]


def col_break_indices(lines, combine='update'):
    """
    Given a set of horizontal separator lines, return a guess as to
    which indices have column breaks, based on common indicator characters.
    """
    all_lines_indices = [vertical_sep_in_line(line) for line in lines]
    combined = intspan(all_lines_indices[0])
    update_func = getattr(combined, combine)
    for line_indices in all_lines_indices[1:]:
        update_func(line_indices)
    return combined


def find_columns(lines):
    """
    Given a list of text lines, assume they represent a fixed-width
    "ASCII table" and guess the column indices therein. Depends on
    finding typographical "rivers" of spaces running vertically
    through text indicating column breaks.

    This is a high-probability heuristic. There are some cases
    where all rows happen to include aligned spaces that do *not*
    signify a column break. In this case, recommend you modify the
    table with a separator line (e.g. using --- characters showing)
    where the columns should be. Since separators are stripped out,
    adding an explicit set of separators will not alter the result data.
    """
    # Partition lines into seps (separators and blank lines) and nonseps (content)
    seps, nonseps = [], []
    for line in lines:
        if is_separator(line):
            seps.append(line)
        else:
            nonseps.append(line)

    # Find max length of content lines. This defines the "universe" of
    # available content columns.
    maxlen = max(len(l) for l in nonseps)
    universe = intspan.from_range(0, maxlen - 1)

    if seps:
        # If separators, try to find the column breaks in them
        indices = col_break_indices(seps)
        iranges = (universe - indices).ranges()

    if not seps or (seps and not indices):
        # If horizontal separators not present, or if present but lack the vertical
        # separation indicators needed to determine column locations, look for
        # vertical separators common to all rows. This a rare, but genuine case.
        indices = col_break_indices(nonseps, 'intersection_update')
        if indices:
            iranges = (universe - indices).ranges()
        else:
            # No common vertical separators to speak of. Fall back to
            # using vertical whitespace rivers as column separators.
            # Find where spaces are in every column.
            spaces = intspan.from_range(0, maxlen - 1)
            for l in nonseps:
                line_spaces = intspan(all_indices(l, ' '))
                spaces.intersection_update(line_spaces)
            # Spaces is now intspan showing where spaces are
            # Find inclusive ranges wehre content would be
            iranges = (universe - spaces).ranges()

    # Convert inclusive ranges to half-open Python ranges
    hranges = [(s, e+1) for s,e in iranges]
    return seps, nonseps, hranges


def discover_table(text, evaluate=True, cstrip=True):
    """
    Return a list of lists representing a table.
    """

    if cstrip:
        text = CSTRIP.sub('', text)

    # import text into lines
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]

    # remove common indentation (needs round trip back to string, then to lines)
    cleanlines = '\n'.join(lines)
    lines = textwrap.dedent(cleanlines).splitlines()

    # find the columns
    seps, nonseps, column_indices = find_columns(lines)
    n_columns = len(column_indices)

    # extend evaluate for each column, as needed
    if isinstance(evaluate, (list, tuple)):
        # already a sequence; determine if needs extension
        needed = n_columns - len(evaluate)
        if needed > 0:
            evaluates = list(evaluate) + ([evaluate[-1]] * needed)
        else:
            evaluates = evaluate[:]
    else:
        # multiple scalar to n_columns copies
        evaluates = [evaluate] * n_columns

    # construct table based on discovered understanding
    # of where column breaks are
    rows = []
    for l in nonseps:
        row = []
        for r, col_evaluate in zip(column_indices, evaluates):
            segment = l[r[0]:r[1]]
            print('segment:', repr(segment))
            row.append(evaluation(segment, col_evaluate))
        rows.append(row)
    return rows


def table(text, header=None, evaluate=True, cstrip=True):
    """
    Return a list of lists representing a table.

    Args:
        text (basestring): text in which to find table
        header (str|list|None): Header for the table
        evaluate (Union[str, function, None]): Indicates how to post-process
            table cells. By default, True or "natural" means as Python literals.
            Other options are False or 'minimal' (just string trimming), or
            None or 'none'.  Can also provide a custom function.
        cstrip (bool): strip comments?
    Returns:
        List of lists, where each inner list represents a row.
    """

    rows = discover_table(text, evaluate, cstrip)

    if header:
        if isinstance(header, basestring):
            header = header.split()
        if isinstance(header, list):
            rows.insert(0, header)

    return rows

# add converters / data type setters and date guesser
# add auto interpretation of column headers (heuristic)


def records(t, dict=dict, keyclean=None, **kwargs):
    rows = table(t, **kwargs)
    header, rows = rows[0], rows[1:]
    if keyclean:
        header = [keyclean(h) for h in header]

    return [dict(zip(header, row)) for row in rows]


if __name__ == '__main__':   # pragma: no cover
    from pprint import pprint
    import sys
    sys.path.insert(0, '../test')
    from test_table import samples


    text="""
+-----------+--------+-------------+------------------------+---------+
| User Name | Salary | Designation |         Address        |  Lucky# |
+-----------+--------+-------------+------------------------+---------+
|       Ram |   2000 |     Manager |        #99, Silk board |    1111 |
|       Sri |  12000 |   Developer |             BTM Layout |   22222 |
|    Prasad |  42000 |        Lead | #66, Viaya Bank Layout |  333333 |
|       Anu | 132000 |          QA |             #22, Vizag | 4444444 |
|       Sai |  62000 |   Developer |         #3-3, Kakinada |         |
|    Venkat |   2000 |     Manager |                        |         |
|       Raj |  62000 |             |                        |         |
|       BTC |        |             |                        |         |
+-----------+--------+-------------+------------------------+---------+
"""
    expected=[
            ['User Name', 'Salary', 'Designation', 'Address', 'Lucky#'],
            ['Ram', 2000, 'Manager', '#99, Silk board', 1111],
            ['Sri', 12000, 'Developer', 'BTM Layout', 22222],
            ['Prasad', 42000, 'Lead', '#66, Viaya Bank Layout', 333333],
            ['Anu', 132000, 'QA', '#22, Vizag', 4444444],
            ['Sai', 62000, 'Developer', '#3-3, Kakinada', ''],
            ['Venkat', 2000, 'Manager', '', ''],
            ['Raj', 62000, '', '', ''],
            ['BTC', '', '', '', '']
        ]
    pprint(table(text))

    if False:
        # multi table test
        count = 0
        from tabsample import samples
        for t in samples:
            # if t.expected:
            #     continue
            print()
            print('Name:  ', t.name)
            # print('Source:', t.source)
            print()
            print(t.text)
            print()
            options = t.options if hasattr(t, 'options') else {}
            rows = table(t.text, **options)
            pprint(rows)
            if t.expected:
                assert rows == t.expected
                count += 1

            print()
            print('===')
            print()
        print()
        print(count, 'successful tests')

    if False:

        from textdata.attrs import Dict

        from collections import OrderedDict
        t5 = getattr(tabsample, 't5')
        pprint(records(t5))
        print('---')
        pprint(records(t5, dict=OrderedDict))
        print('---')
        pprint(records(t5, dict=Dict))
        print('---')
        kc = lambda h: h.lower().replace(' ', '_')
        # https://pypi.python.org/pypi/pydentifier/0.1.3
        # for the full identifier cleanup
        pprint(records(t5, dict=Dict, keyclean=kc))
