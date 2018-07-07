# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals

from textdata import *
from pprint import pprint
from datetime import datetime, date
import sys
import pytest


_PY2 = sys.version_info[0] == 2

def test_custom_header():
    source = """
        Joe   12   woodworking
        Jill  12   slingshot
        Meg   13   snark, snapchat
    """
    t1 = table(source)
    assert t1 == [['Joe', 12, 'woodworking'],
                  ['Jill', 12, 'slingshot'],
                  ['Meg', 13, 'snark, snapchat']]

    # use words() for splitting string
    t2 = table(source, 'name age "favorite hobbies"') 
    assert t2 == [['name', 'age', 'favorite hobbies'],
                  ['Joe', 12, 'woodworking'],
                  ['Jill', 12, 'slingshot'],
                  ['Meg', 13, 'snark, snapchat']]

    t3 = table(source, header=['name', 'age', "favorite hobbies"])
    assert t2 == t3

    source2 = """
    |--:|----:|----|-----|-------:|----------|
    |  0| 0.10|hoge|True |       0|2017-01-01|
    |  2|-2.23|foo |False|        |2017-12-23|
    |  3| 0.00|bar |True |      33|2017-03-03|
    |-10|-9.90|    |False|    50.5|2017-01-01|
    """

    import datetime
    dateparse = lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date()
    floatparse = lambda s, empty=0.0: float(s) if s.strip() else empty
    t4 = table(source2, evaluate=('natural', 'natural', str, 'natural', floatparse, dateparse))
    assert t4 == [[0, 0.1, 'hoge', True, 0.0, datetime.date(2017, 1, 1)],
                  [2, -2.23, 'foo ', False, 0.0, datetime.date(2017, 12, 23)],
                  [3, 0.0, 'bar ', True, 33.0, datetime.date(2017, 3, 3)],
                  [-10, -9.9, '    ', False, 50.5, datetime.date(2017, 1, 1)]]

    source3 = """
    |int|float|str |bool |     mix|date      |
    |--:|----:|----|-----|-------:|----------|
    |  0| 0.10|hoge|True |       0|2017-01-01|
    |  2|-2.23|foo |False|        |2017-12-23|
    |  3| 0.00|bar |True |      33|2017-03-03|
    |-10|-9.90|    |False|    50.5|2017-01-01|
    """
    t5 = table(source3, header=True, evaluate=('natural', 'natural', str, 'natural', floatparse, dateparse))
    assert t5 == [['int', 'float', 'str', 'bool', 'mix', 'date'],
                  [0, 0.1, 'hoge', True, 0.0, datetime.date(2017, 1, 1)],
                  [2, -2.23, 'foo ', False, 0.0, datetime.date(2017, 12, 23)],
                  [3, 0.0, 'bar ', True, 33.0, datetime.date(2017, 3, 3)],
                  [-10, -9.9, '    ', False, 50.5, datetime.date(2017, 1, 1)]]


def test_multiple_evaluates():
    source = """
        Joe   12   woodworking
        Jill  12   slingshot
        Meg   13   snark, snapchat
    """
    t1 = table(source, evaluate=(lambda s: s.strip().upper(), float, 'minimal'))    
    assert t1 == [['JOE', 12.0, 'woodworking'],
                  ['JILL', 12.0, 'slingshot'],
                  ['MEG', 13.0, 'snark, snapchat']]

    t2 = table(source, evaluate=(lambda s: s.strip().upper(), float))
    assert t1 == t2


samples = [
    Dict(name='t000',
         source='unknown',
         text="""
    0     ape    dog       3
    1     ape   hors       3
    8     dog   hors       2
    2     ape     la       1
        """,
         expected=[
            [0, 'ape', 'dog', 3],
            [1, 'ape', 'hors', 3],
            [8, 'dog', 'hors', 2],
            [2, 'ape', 'la', 1]
        ]
    ),
    Dict(name="t001",
         source="https://www.npmjs.com/package/text-table",
         text= """

        beep   1024
        boop  33450
        foo    1006
        bar      45

        """,
        expected=[
            ['beep', 1024],
            ['boop', 33450],
            ['foo', 1006],
            ['bar', 45]
        ]
    ),
    Dict(name='t002',
         source="https://www.npmjs.com/package/text-table",
         text="""
beep  1024
boop   334.212
foo   1006
bar     45.6
baz    123.
""",
        expected=[
            ['beep', 1024],
            ['boop', 334.212],
            ['foo', 1006],
            ['bar', 45.6],
            ['baz', 123.0]
        ],
    ),
    Dict(name="t003",
         source="https://www.npmjs.com/package/text-table",
         text="""
master   0123456789abcdef
staging  fedcba9876543210
""",
         expected=[
            ['master', '0123456789abcdef'],
            ['staging', 'fedcba9876543210']
        ]
    ),
    Dict(name="t003a",
         source="https://www.npmjs.com/package/text-table",
         text="""
master   0123456789abcdef   # is comment
staging  fedcba9876543210   # this too
""",
         options=dict(cstrip=True),
         expected=[
            ['master', '0123456789abcdef'],
            ['staging', 'fedcba9876543210']
        ]
    ),
    Dict(name="t003b",
         source="https://www.npmjs.com/package/text-table",
         text="""
master   0123456789abcdef   # is comment
staging  fedcba9876543210   # this too
""",
         options=dict(header='name key'),
         expected=[
            ['name', 'key'],
            ['master', '0123456789abcdef'],
            ['staging', 'fedcba9876543210']
        ]
    ),
    Dict(name="t003c",
         source="https://www.npmjs.com/package/text-table",
         text="""
master   0123456789abcdef   # not comment
staging  fedcba9876543210   # this too
""",
         options=dict(cstrip=False),
         expected=[
            ['master', '0123456789abcdef', '#', 'not comment'],
            ['staging', 'fedcba9876543210', '#', 'this too']
        ]
    ),
    Dict(name="t004",
         source="http://search.cpan.org/~shlomif/Text-Table-1.133/lib/Text/Table.pm",
         text="""
  Planet  Radius Density
          km     g/cm^3
  Mercury  2360  3.7
  Venus    6110  5.1
  Earth    6378  5.52
  Jupiter 71030  1.3
""",
         expected=[
            ['Planet', 'Radius', 'Density'],
            ['', 'km', 'g/cm^3'],
            ['Mercury', 2360, 3.7],
            ['Venus', 6110, 5.1],
            ['Earth', 6378, 5.52],
            ['Jupiter', 71030, 1.3]
        ]
    ),
    Dict(name="t004a",
         source="http://search.cpan.org/~shlomif/Text-Table-1.133/lib/Text/Table.pm",
         text="""
  Planet  Radius Density
          km     g/cm^3
  ------- -----  -------
  Mercury  2360  3.7
  Venus    6110  5.1
  Earth    6378  5.52
  Jupiter 71030  1.3
""",
         expected=[
            ['Planet', 'Radius', 'Density'],
            ['', 'km', 'g/cm^3'],
            ['Mercury', 2360, 3.7],
            ['Venus', 6110, 5.1],
            ['Earth', 6378, 5.52],
            ['Jupiter', 71030, 1.3]
        ]
    ),
    Dict(name="t005",
         source="unknown",
         text="""
  Day     Hour     Name     Msg
sunday     10        a       b
sunday     11        a       b
sunday     11        a       b
monday     12        a       b
tuesday    10        a       b
tuesday    10        a       b
""",
         expected=[
            ['Day', 'Hour', 'Name', 'Msg'],
            ['sunday', 10, 'a', 'b'],
            ['sunday', 11, 'a', 'b'],
            ['sunday', 11, 'a', 'b'],
            ['monday', 12, 'a', 'b'],
            ['tuesday', 10, 'a', 'b'],
            ['tuesday', 10, 'a', 'b']
        ]
    ),
    Dict(name="t005a",
         source="unknown",
         text="""
  Day     Hour     Name     Msg
  ===     ====     ====     ===
sunday     10        a       b
sunday     11        a       b
sunday     11        a       b
monday     12        a       b
tuesday    10        a       b
tuesday    10        a       b
""",
         expected=[
            ['Day', 'Hour', 'Name', 'Msg'],
            ['sunday', 10, 'a', 'b'],
            ['sunday', 11, 'a', 'b'],
            ['sunday', 11, 'a', 'b'],
            ['monday', 12, 'a', 'b'],
            ['tuesday', 10, 'a', 'b'],
            ['tuesday', 10, 'a', 'b']
        ]
    ),
    Dict(name="t006",
         source="http://www.rubydoc.info/gems/text-table/1.2.4",
         text="""
    +----+----+
    | A  | B  |
    +----+----+
    | a1 | b1 |
    | a2 | b2 |
    +----+----+
""",
         expected=[
            ['A', 'B'],
            ['a1', 'b1'],
            ['a2', 'b2']
        ]
    ),
    Dict(name="t007",
         source="http://www.rubydoc.info/gems/text-table/1.2.4",
         text="""
    +---------+-----------+--------+
    | Student | Mid-Terms | Finals |
    | Sam     | 94        | 93     |
    | Jane    | 92        | 99     |
    | Average | 93        | 96     |
    +---------+-----------+--------+
""",
         expected=[
            ['Student', 'Mid-Terms', 'Finals'],
            ['Sam', 94, 93],
            ['Jane', 92, 99],
            ['Average', 93, 96]
        ]
    ),
    Dict(name="t008",
         source="http://www.rubydoc.info/gems/text-table/1.2.4",
         text="""
    +---------+-----------+--------+
    | Student | Mid-Terms | Finals |
    +---------+-----------+--------+
    | Sam     | 94        | 93     |
    | Jane    | 92        | 99     |
    | Average | 93        | 96     |
    +---------+-----------+--------+
""",
         expected=[
            ['Student', 'Mid-Terms', 'Finals'],
            ['Sam', 94, 93],
            ['Jane', 92, 99],
            ['Average', 93, 96]
        ]
    ),
    Dict(name="t009",
         source="http://www.rubydoc.info/gems/text-table/1.2.4",
         text="""
    +---------+-----------+--------+
    | Student | Mid-Terms | Finals |
    +---------+-----------+--------+
    | Sam     | 94        | 93     |
    | Jane    | 92        | 99     |
    +---------+-----------+--------+
    | Average | 93        | 96     |
    +---------+-----------+--------+
""",
         expected=[
            ['Student', 'Mid-Terms', 'Finals'],
            ['Sam', 94, 93],
            ['Jane', 92, 99],
            ['Average', 93, 96]
        ]
    ),
    Dict(name="t010",
         source="https://www.mediawiki.org/wiki/Manual:Text_table",
         text="""
+-----------+-----------------+------+-----+---------+----------------+
| Field     | Type            | Null | Key | Default | Extra          |
+-----------+-----------------+------+-----+---------+----------------+
| old_id    | int(8) unsigned | NO   | PRI | NULL    | AUTO_INCREMENT |
| old_text  | mediumblob      | NO   |     | NULL    |                |
| old_flags | tinyblob        | NO   |     | NULL    |                |
+-----------+-----------------+------+-----+---------+----------------+
""",
         expected=[
            ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'],
            ['old_id', 'int(8) unsigned', 'NO', 'PRI', 'NULL', 'AUTO_INCREMENT'],
            ['old_text', 'mediumblob', 'NO', '', 'NULL', ''],
            ['old_flags', 'tinyblob', 'NO', '', 'NULL', '']
        ]
    ),
    Dict(name="t011",
         source="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#tables",
         text="""
| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

""",
         expected=[
            ['Tables', 'Are', 'Cool'],
            ['col 3 is', 'right-aligned', '$1600'],
            ['col 2 is', 'centered', '$12'],
            ['zebra stripes', 'are neat', '$1']
        ]
    ),
    Dict(name="t012",
         source="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#tables",
         text="""
Markdown | Less      | Pretty
-------- | --------- | ----------
*Still*  | `renders` | **nicely**
1        | 2         | 3
""",
         expected=[
            ['Markdown', 'Less', 'Pretty'],
            ['*Still*', '`renders`', '**nicely**'],
            [1, 2, 3]
        ]
    ),
    Dict(name="t013",
         source="https://www.tablesgenerator.com/text_tables",
         text="""
╔═════════════╦═════╦═══════════════════════════════════════════════════════════════════════╗
║ one         ║ two ║ three                                                                 ║
╠═════════════╬═════╬═══════════════════════════════════════════════════════════════════════╣
║ four things ║ 3   ║ many things go here and there                                         ║
║             ║     ║ are perhaps too many things to fin on one line how does that work out ║
╠═════════════╬═════╬═══════════════════════════════════════════════════════════════════════╣
║ la          ║ la  ║ la                                                                    ║
╚═════════════╩═════╩═══════════════════════════════════════════════════════════════════════╝
""",
         expected=[
            ['one', 'two', 'three'],
            ['four things', 3, 'many things go here and there'],
            ['',
             '',
             'are perhaps too many things to fin on one line how does that work out'],
            ['la', 'la', 'la']
        ]
    ),
    Dict(name="t014",
         source="https://www.postgresql.org/docs/9.1/static/app-psql.html",
         text="""
+-------+--------+
| first | second |
+-------+--------+
|     1 | one    |
|     2 | two    |
|     3 | three  |
|     4 | four   |
+-------+--------+
""",
         expected=[
            ['first', 'second'],
            [1, 'one'],
            [2, 'two'],
            [3, 'three'],
            [4, 'four']
        ]
    ),
    Dict(name="t015",
         source="https://www.postgresql.org/docs/9.1/static/app-psql.html",
         text="""
first second
----- ------
    1 one
    2 two
    3 three
    4 four
""",
         expected=[
            ['first', 'second'],
            [1, 'one'],
            [2, 'two'],
            [3, 'three'],
            [4, 'four']
        ]
    ),
    Dict(name="t016",
         source="https://metacpan.org/pod/Text::Table::Any",
         text="""
+-------+----------+----------+
| Name  | Rank     | Serial   |
+-------+----------+----------+
| alice | pvt      | 123456   |
| bob   | cpl      | 98765321 |
| carol | brig gen | 8745     |
+-------+----------+----------+
""",
         expected=[
            ['Name', 'Rank', 'Serial'],
            ['alice', 'pvt', 123456],
            ['bob', 'cpl', 98765321],
            ['carol', 'brig gen', 8745]]
    ),
    Dict(name="t017",
         source="https://metacpan.org/pod/Text::Table::Any",
         text= """
| Name  | Rank     | Serial   |
|-------+----------+----------|
| alice | pvt      | 123456   |
| bob   | cpl      | 98765321 |
| carol | brig gen | 8745     |
""",
         expected=[
            ['Name', 'Rank', 'Serial'],
            ['alice', 'pvt', 123456],
            ['bob', 'cpl', 98765321],
            ['carol', 'brig gen', 8745]
        ]
    ),
    Dict(name="t018",
         source="https://metacpan.org/pod/Text::Table::Any",
         text="""
.-------+----------+----------.
| Name  | Rank     |   Serial |
+-------+----------+----------+
| alice | pvt      |   123456 |
| bob   | cpl      | 98765321 |
| carol | brig gen |     8745 |
`-------+----------+----------'
"""
,
         expected=[
            ['Name', 'Rank', 'Serial'],
            ['alice', 'pvt', 123456],
            ['bob', 'cpl', 98765321],
            ['carol', 'brig gen', 8745]
        ]
    ),
    Dict(name="t019",
         source="http://search.cpan.org/~lunatic/Text-ASCIITable-0.22/lib/Text/ASCIITable.pm",
         text="""
  .------------------------------.
  |            Basket            |
  +----+-----------------+-------+
  | Id | Name            | Price |
  +----+-----------------+-------+
  |  1 | Dummy product 1 |  24.4 |
  |  2 | Dummy product 2 |  21.2 |
  |  3 | Dummy product 3 |  12.3 |
  +----+-----------------+-------+
  |    | Total           |  57.9 |
  '----+-----------------+-------'
  """,
         expected=[
            ['', 'Basket', ''],
            ['Id', 'Name', 'Price'],
            [1, 'Dummy product 1', 24.4],
            [2, 'Dummy product 2', 21.2],
            [3, 'Dummy product 3', 12.3],
            ['', 'Total', 57.9]
        ]
    ),
    Dict(name="t020",
         source="https://hackage.haskell.org/package/table-layout",
         text="""
┌────────────┬────────────┐
│    Text    │   Number   │
╞════════════╪════════════╡
│ A very lo… │   0.42000… │
├────────────┼────────────┤
│ Short text │ …00.5      │
└────────────┴────────────┘
""",
         expected=[
            ['Text', 'Number'],
            ['A very lo…', '0.42000…'],
            ['Short text', '…00.5']
         ]
    ),
    Dict(name="t021",
         source="https://hackage.haskell.org/package/table-layout",
         text="""
+----------------------------------------------------+--------+
|                        Text                        | Length |
+----------------------------------------------------+--------+
| Lorem  ipsum dolor sit amet, consectetur adipisici |        |
| elit,  sed eiusmod  tempor incidunt  ut labore  et |        |
| dolore magna aliqua. Ut enim ad minim veniam, quis |        |
| nostrud   exercitation  ullamco  laboris  nisi  ut |        |
| aliquid  ex ea  commodi consequat.  Quis aute iure |    429 |
| reprehenderit   in  voluptate  velit  esse  cillum |        |
| dolore  eu fugiat  nulla pariatur.  Excepteur sint |        |
| obcaecat cupiditat non proident, sunt in culpa qui |        |
| officia deserunt mollit anim id est laborum.       |        |
+----------------------------------------------------+--------+
""",
         expected=[
            ['Text', 'Length'],
            ['Lorem  ipsum dolor sit amet, consectetur adipisici', ''],
            ['elit,  sed eiusmod  tempor incidunt  ut labore  et', ''],
            ['dolore magna aliqua. Ut enim ad minim veniam, quis', ''],
            ['nostrud   exercitation  ullamco  laboris  nisi  ut', ''],
            ['aliquid  ex ea  commodi consequat.  Quis aute iure', 429],
            ['reprehenderit   in  voluptate  velit  esse  cillum', ''],
            ['dolore  eu fugiat  nulla pariatur.  Excepteur sint', ''],
            ['obcaecat cupiditat non proident, sunt in culpa qui', ''],
            ['officia deserunt mollit anim id est laborum.', '']
        ]
    ),
    Dict(name="t022",
         source="https://pypi.org/project/plaintable",
         text="""
            one   two   three  four  five
            ----  ----  -----  ----  -----
            1     2     3      4     5
            10    11    12     13    14
            a     b     c      d     e
            1.00  2.00  1.50   4.25  10.50
         """,
         expected=[
            ['one', 'two', 'three', 'four', 'five'],
            [1, 2, 3, 4, 5],
            [10, 11, 12, 13, 14],
            ['a', 'b', 'c', 'd', 'e'],
            [1.0, 2.0, 1.5, 4.25, 10.5]
        ]
    ),
    Dict(name="t023",
         source="http://www.sphinx-doc.org/en/stable/rest.html",
         text="""
    +------------------------+------------+----------+----------+
    | Header row, column 1   | Header 2   | Header 3 | Header 4 |
    | (header rows optional) |            |          |          |
    +========================+============+==========+==========+
    | body row 1, column 1   | column 2   | column 3 | column 4 |
    +------------------------+------------+----------+----------+
    | body row 2             | ...        | ...      |          |
    +------------------------+------------+----------+----------+
         """,
         expected=[
            ['Header row, column 1', 'Header 2', 'Header 3', 'Header 4'],
            ['(header rows optional)', '', '', ''],
            ['body row 1, column 1', 'column 2', 'column 3', 'column 4'],
            ['body row 2', '...', '...', '']
        ]
    ),
    Dict(name="t024",
         source="http://www.sphinx-doc.org/en/stable/rest.html",
         text="""
         =====  =====  =======
         A      B      A and B
         =====  =====  =======
         False  False  False
         True   False  False
         False  True   False
         True   True   True
         =====  =====  =======
         """,
         expected=[
            ['A', 'B', 'A and B'],
            [False, False, False],
            [True, False, False],
            [False, True, False],
            [True, True, True]
        ]
    ),
    Dict(name="t025",
         source="https://www.npmjs.com/package/markdown-tables",
         text="""
| Label          | Square Footage | Color  |
|----------------|----------------|--------|
| Office         | 224            | Blue   |
| Kitchen        | 230            | Green  |
| Clothes Closet | 45             | Yellow |
| Storage Closet | 56             | Red    |
         """,
         expected=[
            ['Label', 'Square Footage', 'Color'],
            ['Office', 224, 'Blue'],
            ['Kitchen', 230, 'Green'],
            ['Clothes Closet', 45, 'Yellow'],
            ['Storage Closet', 56, 'Red']
        ]
    ),
    Dict(name="t026",
         source="https://github.com/ozh/ascii-tables",
         text="""
.----------------------------------.---------.------------------------.----------------.
|               Col1               |  Col2   |          Col3          | Numeric Column |
:----------------------------------+---------+------------------------+----------------:
| Value 1                          | Value 2 | 123                    |           10.0 |
:----------------------------------+---------+------------------------+----------------:
| Separate                         | cols    | with a tab or 4 spaces |       -2,027.1 |
:----------------------------------+---------+------------------------+----------------:
| This is a row with only one cell |         |                        |                |
'----------------------------------'---------'------------------------'----------------'

         """,
         expected=[
            ['Col1', 'Col2', 'Col3', 'Numeric Column'],
            ['Value 1', 'Value 2', 123, 10.0],
            ['Separate', 'cols', 'with a tab or 4 spaces', (-2, 27.1)],
            ['This is a row with only one cell', '', '', '']
        ]
         # This is indeed what's expected, though it isn't what you might want.
         # The error is that Python literal parsing doesn't quite grok the numerical
         # format in the raw text.
    ),
    Dict(name="t026a",
         source="https://github.com/ozh/ascii-tables",
         text="""
.----------------------------------.---------.------------------------.----------------.
|               Col1               |  Col2   |          Col3          | Numeric Column |
:----------------------------------+---------+------------------------+----------------:
| Value 1                          | Value 2 | 123                    |           10.0 |
:----------------------------------+---------+------------------------+----------------:
| Separate                         | cols    | with a tab or 4 spaces |       -2,027.1 |
:----------------------------------+---------+------------------------+----------------:
| This is a row with only one cell |         |                        |                |
'----------------------------------'---------'------------------------'----------------'

         """,
         options=dict(evaluate='minimal'),
         expected=[
            ['Col1', 'Col2', 'Col3', 'Numeric Column'],
            ['Value 1', 'Value 2', '123', '10.0'],
            ['Separate', 'cols', 'with a tab or 4 spaces', '-2,027.1'],
            ['This is a row with only one cell', '', '', '']
        ]
         # Turning off natural interpretation "fixes" the problem.
         # See also https://github.com/ozh/ascii-tables
         # for other examples that don't actually parse. They are not
         # typical ASCII tables, however.
    ),
    Dict(name="t027",
         source="http://docs.astropy.org/en/stable/io/ascii/",
         text="""
         obsid redshift  X    Y      object
         ----- -------- ---- ---- -----------
          3102     0.32 4167 4085 Q1250+568-A
           877     0.22 4378 3892   Source 82
  """,
         expected=[
            ['obsid', 'redshift', 'X', 'Y', 'object'],
            [3102, 0.32, 4167, 4085, 'Q1250+568-A'],
            [877, 0.22, 4378, 3892, 'Source 82']
        ]
    ),
    Dict(name="t028",
         source="http://docs.astropy.org/en/stable/io/ascii/",
         text="""
  objID         osrcid          xsrcid
--------- ----------------- -------------
277955213 S000.7044P00.7513 XS04861B6_005
889974380 S002.9051P14.7003 XS03957B7_004
  """,
         expected=[
            ['objID', 'osrcid', 'xsrcid'],
            [277955213, 'S000.7044P00.7513', 'XS04861B6_005'],
            [889974380, 'S002.9051P14.7003', 'XS03957B7_004']
        ]
    ),
    Dict(name="t029",
         source="http://docs.astropy.org/en/stable/io/ascii/read.html",
         text="""
day  precip type
---- ------ ----
 Mon    1.5 rain
Tues     --   --
 Wed    1.1 snow
  """,
         expected=[
            ['day', 'precip', 'type'],
            ['Mon', 1.5, 'rain'],
            ['Tues', '--', '--'],
            ['Wed', 1.1, 'snow']
        ]
    ),
    Dict(name="t030",
         source="https://stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python",
         text="""
uid   | name       |
------+------------+-
0     | Jon        |
1     | Doe        |
2     | Lemma      |
3     | Hemma      |
------+------------+-""",
         expected=[
            ['uid', 'name'],
            [0, 'Jon'],
            [1, 'Doe'],
            [2, 'Lemma'],
            [3, 'Hemma']
        ]
    ),
    Dict(name="t030",
         source="https://stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python",
         text="""
+----------+------+--------+
|   name   | rank | gender |
+----------+------+--------+
|  Jacob   |  1   |  boy   |
+----------+------+--------+
| Isabella |  1   |  girl  |
+----------+------+--------+
|  Ethan   |  2   |  boy   |
+----------+------+--------+
|  Sophia  |  2   |  girl  |
+----------+------+--------+
| Michael  |  3   |  boy   |
+----------+------+--------+
        """,
         expected=[
            ['name', 'rank', 'gender'],
            ['Jacob', 1, 'boy'],
            ['Isabella', 1, 'girl'],
            ['Ethan', 2, 'boy'],
            ['Sophia', 2, 'girl'],
            ['Michael', 3, 'boy']
        ]
    ),
    Dict(name="t031",
         source="https://stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python",
         text="""

pkid                                 | fkn                                  | npi
-------------------------------------+--------------------------------------+----
405fd665-0a2f-4f69-7320-be01201752ec | 8c9949b9-552e-e448-64e2-74292834c73e | 0
5b517507-2a42-ad2e-98dc-8c9ac6152afa | f972bee7-f5a4-8532-c4e5-2e82897b10f6 | 0
2f960dfc-b67a-26be-d1b3-9b105535e0a8 | ec3e1058-8840-c9f2-3b25-2488f8b3a8af | 1
c71b28a3-5299-7f4d-f27a-7ad8aeadafe0 | 72d25703-4735-310b-2e06-ff76af1e45ed | 0
3b0a5021-a52b-9ba0-1439-d5aafcf348e7 | d81bb78a-d984-e957-034d-87434acb4e97 | 1
96c36bb7-c4f4-2787-ada8-4aadc17d1123 | c171fe85-33e2-6481-0791-2922267e8777 | 1
95d0f85f-71da-bb9a-2d80-fe27f7c02fe2 | 226f964c-028d-d6de-bf6c-688d2908c5ae | 1
132aa774-42e5-3d3f-498b-50b44a89d401 | 44e31f89-d089-8afc-f4b1-ada051c01474 | 1
ff91641a-5802-be02-bece-79bca993fdbc | 33d8294a-053d-6ab4-94d4-890b47fcf70d | 1
f3196e15-5b61-e92d-e717-f00ed93fe8ae | 62fa4566-5ca2-4a36-f872-4d00f7abadcf | 1
        """,
         expected= [['pkid', 'fkn', 'npi'],
                    ['405fd665-0a2f-4f69-7320-be01201752ec',
                     '8c9949b9-552e-e448-64e2-74292834c73e',
                     0],
                    ['5b517507-2a42-ad2e-98dc-8c9ac6152afa',
                     'f972bee7-f5a4-8532-c4e5-2e82897b10f6',
                     0],
                    ['2f960dfc-b67a-26be-d1b3-9b105535e0a8',
                     'ec3e1058-8840-c9f2-3b25-2488f8b3a8af',
                     1],
                    ['c71b28a3-5299-7f4d-f27a-7ad8aeadafe0',
                     '72d25703-4735-310b-2e06-ff76af1e45ed',
                     0],
                    ['3b0a5021-a52b-9ba0-1439-d5aafcf348e7',
                     'd81bb78a-d984-e957-034d-87434acb4e97',
                     1],
                    ['96c36bb7-c4f4-2787-ada8-4aadc17d1123',
                     'c171fe85-33e2-6481-0791-2922267e8777',
                     1],
                    ['95d0f85f-71da-bb9a-2d80-fe27f7c02fe2',
                     '226f964c-028d-d6de-bf6c-688d2908c5ae',
                     1],
                    ['132aa774-42e5-3d3f-498b-50b44a89d401',
                     '44e31f89-d089-8afc-f4b1-ada051c01474',
                     1],
                    ['ff91641a-5802-be02-bece-79bca993fdbc',
                     '33d8294a-053d-6ab4-94d4-890b47fcf70d',
                     1],
                    ['f3196e15-5b61-e92d-e717-f00ed93fe8ae',
                     '62fa4566-5ca2-4a36-f872-4d00f7abadcf',
                     1]
                ]
    ),
    Dict(name="t032",
         source="https://stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python",
         text="""
┌─────┬───────┬─────┐
│first│second │third│
├─────┼───────┼─────┤
│1    │2      │3    │
├─────┼───────┼─────┤
│4    │5      │6    │
└─────┴───────┴─────┘""",
         expected=[
            ['first', 'second', 'third'],
            [1, 2, 3],
            [4, 5, 6]
        ]
    ),
    Dict(name="t033",
         source="https://stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python",
         text="""
┌───────┬─┐
│ first │1│
├───────┼─┤
│second │2│
├───────┼─┤
│ third │3│
└───────┴─┘
""",
         expected=[
            ['first', 1],
            ['second', 2],
            ['third', 3]
        ]
    ),
    Dict(name="t034",
         source="http://docs.astropy.org/en/v0.2.1/_generated/astropy.io.ascii.fixedwidth.FixedWidth.html#astropy.io.ascii.fixedwidth.FixedWidth",
         text="""
|  Col1 |   Col2      |  Col3 |
|  1.2  | hello there |     3 |
|  2.4  | many words  |     7 |
""",
         expected=[
            ['Col1', 'Col2', 'Col3'],
            [1.2, 'hello there', 3],
            [2.4, 'many words', 7]
        ]

    ),
    Dict(name="t035",
         source="https://stackoverflow.com/questions/23165283/formatting-a-text-table-with-fixed-width-columns",
         text="""
Code(ID)    Name            Quantity    SoldQuantity

     001    Tablets                5               3
     002    pens                   4               1
     005    Computeres             3               0
     003    Bages                  2               1
     004    USB                    4               0""",
         expected=[
            ['Code(ID)', 'Name', 'Quantity', 'SoldQuantity'],
            ['001',     'Tablets', 5, 3],
            ['002', 'pens', 4, 1],
            ['005', 'Computeres', 3, 0],
            ['003', 'Bages', 2, 1],
            ['004', 'USB', 4, 0]
        ]
    ),
    Dict(name="t036",
         source="https://stackoverflow.com/questions/23165283/formatting-a-text-table-with-fixed-width-columns",
         text="""
┌─────────┬─────────────────────────────────────────────────────────────────────────┬────────────────────────────┐
│ Command │ Description                                                             │ Syntax                     │
┢━━━━━━━━━╈━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╈━━━━━━━━━━━━━━━━━━━━━━━━━━━━┪
┃ bye     ┃ Quits the application.                                                  ┃                            ┃
┃ ga      ┃ Adds the specified game.                                                ┃ <id> <description> <path>  ┃
┃ gl      ┃ Lists all currently added games                                         ┃ [pattern]                  ┃
┃ gr      ┃ Rebuilds the files of the currently active game.                        ┃                            ┃
┃ gs      ┃ Selects the specified game.                                             ┃ <id>                       ┃
┃ help    ┃ Lists all available commands.                                           ┃ [pattern]                  ┃
┃ license ┃ Displays licensing info.                                                ┃                            ┃
┃ ma      ┃ Adds a mod to the currently active game.                                ┃ <id> <file>                ┃
┃ md      ┃ Deletes the specified mod and removes all associated files.             ┃ <id>                       ┃
┃ me      ┃ Toggles if the selected mod is active.                                  ┃ <id>                       ┃
┃ ml      ┃ Lists all mods for the currently active game.                           ┃ [pattern]                  ┃
┃ mm      ┃ Moves the specified mod to the specified position in the priority list. ┃ <id> <position>            ┃
┃ top kek ┃ Test command. Do not use, may cause death and/or destruction            ┃                            ┃
┃ ucode   ┃ Toggles advanced unicode. (Enhanced characters)                         ┃ [on|true|yes|off|false|no] ┃
┗━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
""",
         expected=[['Command', 'Description', 'Syntax'],
            ['bye', 'Quits the application.', ''],
            ['ga', 'Adds the specified game.', '<id> <description> <path>'],
            ['gl', 'Lists all currently added games', '[pattern]'],
            ['gr', 'Rebuilds the files of the currently active game.', ''],
            ['gs', 'Selects the specified game.', '<id>'],
            ['help', 'Lists all available commands.', '[pattern]'],
            ['license', 'Displays licensing info.', ''],
            ['ma', 'Adds a mod to the currently active game.', '<id> <file>'],
            ['md', 'Deletes the specified mod and removes all associated files.', '<id>'],
            ['me', 'Toggles if the selected mod is active.', '<id>'],
            ['ml', 'Lists all mods for the currently active game.', '[pattern]'],
            ['mm',
             'Moves the specified mod to the specified position in the priority list.',
             '<id> <position>'],
            ['top kek',
             'Test command. Do not use, may cause death and/or destruction',
             ''],
            ['ucode',
             'Toggles advanced unicode. (Enhanced characters)',
             '[on|true|yes|off|false|no]']
        ]
    ),
    Dict(name="t036a",
         source="https://stackoverflow.com/questions/23165283/formatting-a-text-table-with-fixed-width-columns",
         text="""
Command | Description                                                             | Syntax
--------+-------------------------------------------------------------------------+---------------------------
bye     | Quits the application.                                                  |
ga      | Adds the specified game.                                                | <id> <description> <path>
gl      | Lists all currently added games                                         | [pattern]
gr      | Rebuilds the files of the currently active game.                        |
gs      | gs      | Selects the specified gamSelects the specified game.                                             | <id>
help    | Lists all available commands.                                           | [pattern]
license | Displays licensing info.                                                |
ma      | Adds a mod to the currently active game.                                | <id> <file>
md      | Deletes the specified mod and removes all associated files.             | <id>
me      | Toggles if the selected mod is active.                                  | <id>
ml      | Lists all mods for the currently active game.                           | [pattern]
mm      | Moves the specified mod to the specified position in the priority list. | <id> <position>
top kek | Test command. Do not use, may cause death and/or destruction            |
ucode   | Toggles advanced unicode. (Enhanced characters)                         | [on|true|yes|off|false|no]
""",
         expected=[
            ['Command', 'Description', 'Syntax'],
            ['bye', 'Quits the application.', ''],
            ['ga', 'Adds the specified game.', '<id> <description> <path>'],
            ['gl', 'Lists all currently added games', '[pattern]'],
            ['gr', 'Rebuilds the files of the currently active game.', ''],
            ['gs',
             'gs      | Selects the specified gamSelects the specified game.',
             '| <id>'],
            ['help', 'Lists all available commands.', '[pattern]'],
            ['license', 'Displays licensing info.', ''],
            ['ma', 'Adds a mod to the currently active game.', '<id> <file>'],
            ['md', 'Deletes the specified mod and removes all associated files.', '<id>'],
            ['me', 'Toggles if the selected mod is active.', '<id>'],
            ['ml', 'Lists all mods for the currently active game.', '[pattern]'],
            ['mm',
             'Moves the specified mod to the specified position in the priority list.',
             '<id> <position>'],
            ['top kek',
             'Test command. Do not use, may cause death and/or destruction',
             ''],
            ['ucode',
             'Toggles advanced unicode. (Enhanced characters)',
             '[on|true|yes|off|false|no]']
        ]
    ),
    Dict(name="t037",
         source="http://bethecoder.com/applications/products/asciiTable.action",
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
""",
         options=dict(cstrip=False),
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
    ),
    Dict(name="t038",
         source="homegrown",
         text="""
    name  age  strengths
    ----  ---  ---------
    Joe   12   woodworking

    Jill  12   slingshot

    Meg   13   snark, snapchat
""",
         expected=[
            ['name', 'age', 'strengths'],
            ['Joe', 12, 'woodworking'],
            ['Jill', 12, 'slingshot'],
            ['Meg', 13, 'snark, snapchat'],
        ]
    ),
    Dict(name="t038a",
         source="homegrown",
         text="""
    Joe   12   woodworking
    Jill  12   slingshot
    Meg   13   snark, snapchat
""",
         options = dict(header='name age strengths'),
         expected=[
            ['name', 'age', 'strengths'],
            ['Joe', 12, 'woodworking'],
            ['Jill', 12, 'slingshot'],
            ['Meg', 13, 'snark, snapchat'],
        ]
    ),
    Dict(name="t038b",
         source="homegrown",
         text="""
    Joe   12   woodworking
    Jill  12   slingshot
    Meg   13   snark, snapchat
""",
         options = dict(header='name age strengths'.split()),
         expected=[
            ['name', 'age', 'strengths'],
            ['Joe', 12, 'woodworking'],
            ['Jill', 12, 'slingshot'],
            ['Meg', 13, 'snark, snapchat'],
        ]
    ),
    Dict(name="t039",
         source="homegrown",
         text="""
    Joe   12.3   2017-10-27
    Jill  12.9   2017-09-11
    Meg   13.2   2017-10-16
""",
         options = dict(header='name age joined', evaluate=False),
         expected=[
            ['name', 'age', 'joined'],
            ['Joe', '12.3', '2017-10-27'],
            ['Jill', '12.9', '2017-09-11'],
            ['Meg', '13.2', '2017-10-16'],
        ]
    ),
    Dict(name="t039a",
         source="homegrown",
         text="""
    Joe   12.3   2017-10-27
    Jill  12.9   2017-09-11
    Meg   13.2   2017-10-16
""",
         options = dict(header='name age joined',
                        evaluate=['natural', 'natural']
                        ),
         expected=[
            ['name', 'age', 'joined'],
            ['Joe', 12.3, '2017-10-27'],
            ['Jill', 12.9, '2017-09-11'],
            ['Meg', 13.2, '2017-10-16'],
        ]
    ),
    Dict(name="t039b",
         source="homegrown",
         text="""
    Joe   12.3   2017-10-27
    Jill  12.9   2017-09-11
    Meg   13.2   2017-10-16
""",
         options = dict(header='name age joined',
                        evaluate=[str, float, 'natural']
                        ),
         expected=[
            ['name', 'age', 'joined'],
            ['Joe', 12.3, '2017-10-27'],
            ['Jill', 12.9, '2017-09-11'],
            ['Meg', 13.2, '2017-10-16'],
        ]
    ),
    Dict(name="t039c",
         source="homegrown",
         text="""
    Joe   12.3   2017-10-27
    Jill  12.9   2017-09-11
    Meg   13.2   2017-10-16
""",
         options = dict(header='name age joined',
                        evaluate=[str, float,
                                  lambda d: datetime.strptime(d, '%Y-%m-%d').date()]
                        ),
         expected=[
            ['name', 'age', 'joined'],
            ['Joe', 12.3, date(2017, 10, 27)],
            ['Jill', 12.9, date(2017, 9, 11)],
            ['Meg', 13.2, date(2017, 10, 16)],
        ]
    ),
    Dict(name="t039d",
         source="homegrown",
         text="""
    Joe   12.3   2017-10-27
    Jill  12.9   2017-09-11
    Meg   13.2   2017-10-16
""",
         options = dict(header='name age joined',
                        evaluate=[str, float, float]
                        # final float should fail to evaluate
                        # rendering a string instead
                        ),
         expected=[
            ['name', 'age', 'joined'],
            ['Joe', 12.3, '2017-10-27'],
            ['Jill', 12.9, '2017-09-11'],
            ['Meg', 13.2, '2017-10-16'],
        ]
    ),
]


def test_records():
    text = """
    name  age  strengths
    ----  ---  ---------
    Joe   12   woodworking
    Jill  12   slingshot
    Meg   13   snark, snapchat
    """

    expected = [
        dict(name='Joe', age=12, strengths='woodworking'),
        dict(name='Jill', age=12, strengths='slingshot'),
        dict(name='Meg', age=13, strengths='snark, snapchat'),
    ]

    result = records(text)
    assert result == expected

    text2 = """
    NAME  AGE  STRENGTHS
    ----  ---  ---------
    Joe   12   woodworking
    Jill  12   slingshot
    Meg   13   snark, snapchat
    """
    result2 = records(text2, keyclean=lambda k: k.lower())
    assert result2 == expected

    result3 = records(text, dict=Dict)
    expected3 = [
        Dict(name='Joe', age=12, strengths='woodworking'),
        Dict(name='Jill', age=12, strengths='slingshot'),
        Dict(name='Meg', age=13, strengths='snark, snapchat'),
    ]
    assert result3 == expected3
    assert all(isinstance(r, Dict) for r in result3)

"""
ITEM TEMPLATE (for cut and paste)

    Dict(name="",
         source="",
         text=,
         expected=None
    ),
"""

# create pytest parameterize friendly version of samples
psamples = [(t.name, t.text, getattr(t, 'options', {}), t.expected)
            for t in samples]

@pytest.mark.parametrize("name,text,options,expected", psamples)
def test_table(name, text, options, expected):
    if not options.get('active'):
        return
    result = table(text, **options)
    if _PY2:
        py2_patches(name, expected)
    assert result == expected


def py2_patches(name, expected):
    """
    Expected is a mutable structure. If there are any known patches
    needed for Python 2. this routine mutates expected as needed to
    comport with Python 2 expectations. This style of patch-up is
    superior, because the patches are quite rare.
    """
    if name == 't035':
        for r in expected:
            if r[0].startswith('0'):
                r[0] = int(r[0].lstrip('0'))



"""
Places this will always fall down:
1. When values are not compatible with Python literals. Numerical values
   like -3,121.33 for example, because of the comma.
2. Odd table formats that use different kinds of separators we don't expect.
   Standard Markdown, RST, or ASCII table formats based on conventional usage?
   Great. But start using /// as your separators, or [ as your columne marker,
   or...things outside the norm of ASCII table formatting won't be recognized.
3. Tables with column and row spans, or with multiple rows that wrap text in
   a column (this latter sub-case may work, but won't fully interpret the text
   the way a human would).
4. Does not handle ANSI colored text or table titles embedded in headers,
   a la https://github.com/Robpol86/terminaltables
5. Specialed table formats with extra metadata, such as the IPAC table format
   http://irsa.ipac.caltech.edu/applications/DDGEN/Doc/ipac_tbl.html
   but may handle the tabluar component of same.
6. Note that literals don't parse exactly the same in Python 2 and 3.
   Similar...but not exact. For example, integers with leading zeros are
   permitted in Python 2, but not 3. So Python 2 'natual' will convert '001' to
   1, whereas Python 3, not recognizing '001' as valid, keeps it a string.
"""
