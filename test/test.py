# -*- coding: utf-8 -*-

from textdata import *
from textdata.core import ensure_text, noquotes
import sys
import six


def _print(*args, **kwargs):
    """
    Python 2 and 3 compatible print function, similar to Python 3 arg handling.
    """
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    f   = kwargs.get('file', sys.stdout)
    parts = [str(item) for item in args]
    parts.append(end)
    f.write(sep.join(parts))


def single_trial(name, t, **kwargs):
    _print("---", name, "---")
    reslines = lines(t, **kwargs)
    for line in reslines:
        _print(line)
    _print("--- end", name, "---")

    _print()


def test_ensure_text():
    assert ensure_text("this") == "this"
    assert ensure_text("this is a".split()) == "this\nis\na"


def test_noquotes():
	assert noquotes('"this"') == 'this'
	assert noquotes("'this'") == 'this'
	assert noquotes('this') == 'this'


def test_basic():

    assert lines("""
                 a
                 line
                 or
                 two""") == ['a', 'line', 'or', 'two']


def test_lines_take_lines():
    """
    Ensure that lines() treats data coming in as line lists just as it
    would text.
    """
    assert lines(['a', 'line', 'or', 'two']) == ['a', 'line', 'or', 'two']
    assert lines(['', 'a', 'line', '   ', 'or', 'two', '\n']) == ['a', 'line', 'or', 'two']


def test_encoding():
    assert lines(u"⍟\n★") == [six.u('\u235F'), six.u('\u2605')]
    # took py32 out of testing matrix because this test is too
    # hard to state with it in


def test_lstrip_and_rstrip():
    s = "  a \n b\n c\t\nd"
    assert lines(s, lstrip=True, rstrip=False) == ['a ', 'b', 'c      ', 'd']
    assert lines(s, lstrip=False, rstrip=True) == ['  a', ' b', ' c', 'd']
    assert lines(s, lstrip=True, rstrip=True) == ['a', 'b', 'c', 'd']


def test_mixed_indent():

    assert lines("""
    This is a test of lines
    these should all
    be nice and dedented
        except this one, which has a little non-common space
    ok?
    because ends with more than one blank line, those will be captured


          """) == \
        ['This is a test of lines',
         'these should all',
         'be nice and dedented',
         '    except this one, which has a little non-common space',
         'ok?',
         'because ends with more than one blank line, those will be captured']


def test_noblanks_false():

    assert lines("""
    This is a test of lines
    these should all
    be nice and dedented
        except this one, which has a little non-common space
    ok?
    because ends with more than one blank line, those will be captured


          """, noblanks=False) == \
        ['This is a test of lines',
         'these should all',
         'be nice and dedented',
         '    except this one, which has a little non-common space',
         'ok?',
         'because ends with more than one blank line, those will be captured',
         '',
         '']


def test_cstrip():

    t = """
        this

            is
        ok

    """

    tc = """
        this  # look, a comment!
# more comment
            is
        ok    # other comment
   #comment
    """

    assert lines(t) == lines(tc)
    assert textlines(t) == textlines(tc)


def test_malindented_blank_lines():

    assert textlines(noblanks=False, source="""
        this

        is
        ok

    """) == "this\n\nis\nok\n"


def test_extra_start_space():

    single_trial('test2', """


    This is a test of lines

    here there should be no blanks
     but some that start wiht a little extra space ok?
      which isn't common



          """) == \
        ['This is a test of lines',
         'here there should be no blanks',
         ' but some that start wiht a little extra space ok?',
         "  which isn't common"]


def test_textlines():
    data = """


    This is a test of lines

    here there should be no blanks
     but some that start wiht a little extra space ok?
      which isn't common



          """

    assert lines(data) == textlines(data).splitlines()
    assert lines(data, join=True) == lines(data, join='')
    assert lines(data, join=True) == ''.join(textlines(data).splitlines())
    assert lines(data, join=' ') == ' '.join(textlines(data).splitlines())
    assert lines(data, join='\n') == textlines(data)
    assert len(lines(data)) == 4


def test_text_and_textlines():
    data = """


    This is a test of lines

    here there should be no blanks
     but some that start wiht a little extra space ok?
      which isn't common



          """

    assert lines(data) == text(data).splitlines()
    assert lines(data, join=True) == lines(data, join='')
    assert lines(data, join=True) == ''.join(text(data).splitlines())
    assert lines(data, join=' ') == ' '.join(text(data).splitlines())
    assert lines(data, join='\n') == text(data)
    assert len(lines(data)) == 4


def test_tricky_prefix():
    """
    Common prefixes need not be all spaces. This tests if common non-blank
    prefixes are properly handled.
    """

    t = textlines("""
        something
        something else
    """)
    assert t == "something\nsomething else"

    t2 = textlines("""
xxx y
xxx z
""")
    assert t2 == "xxx y\nxxx z"


def test_words():

    assert words('a b c') == 'a b c'.split()
    assert words(' a b c') == 'a b c'.split()
    assert words('  a  b   c   ') == 'a b c'.split()
    assert words(' Billy Bobby "Mr. Smith"') == ['Billy', 'Bobby', 'Mr. Smith']
    assert words(' Billy Bobby "Mr. Smith" "Mrs. Jones"  ') == \
        ['Billy', 'Bobby', 'Mr. Smith', 'Mrs. Jones']
    assert words(' "" " " "  " "   "') == ['', ' ', '  ', '   ']
    assert words("don't be daft") == ["don't", 'be', 'daft']
    assert words(""" "don't be daft" love """) == ["don't be daft", 'love']

    assert words(""" "hey\nthere" joe""") == ['hey\nthere', 'joe']

    assert words("don't be blue") == ["don't", "be", "blue"]

    assert words("don't be blue don't") == ["don't", "be", "blue", "don't"]
    assert words(""" "'this'" works '"great"' """) == \
				 ["'this'", 'works', '"great"']


def test_words_cstrip():
    w = """ this and
            that
            and
            more
        """
    wc = """ this and  # comment
            that  #comment
            and#comment
            more        #comment
        """
    assert words(w) == words(wc)


def test_words_cstrip_example():
    assert words("""
        __pycache__ *.pyc *.pyo     # compilation artifacts
        .hg* .git*                  # repository artifacts
        .coverage                   # code tool artifacts
        .DS_Store                   # platform artifacts
    """) == ['__pycache__', '*.pyc', '*.pyo', '.hg*', '.git*',
             '.coverage', '.DS_Store']

    assert words("""
        __pycache__ *.pyc *.pyo     # compilation artifacts
        .hg* .git*                  # repository artifacts
        .coverage                   # code tool artifacts
        .DS_Store                   # platform artifacts
    """, cstrip=False) == ['__pycache__', '*.pyc', '*.pyo', '#',
             'compilation', 'artifacts', '.hg*', '.git*', '#', 'repository',
             'artifacts', '.coverage', '#', 'code', 'tool',
             'artifacts', '.DS_Store', '#', 'platform', 'artifacts']


def test_paras_example():
    rhyme = """
        Hey diddle diddle,

        The cat and the fiddle,
        The cow jumped over the moon.
        The little dog laughed,
        To see such sport,

        And the dish ran away with the spoon.
    """
    assert paras(rhyme) == \
    [['Hey diddle diddle,'],
     ['The cat and the fiddle,',
      'The cow jumped over the moon.',
      'The little dog laughed,',
      'To see such sport,'],
     ['And the dish ran away with the spoon.']]

    assert paras(rhyme, join="\n") == \
    ['Hey diddle diddle,',
     'The cat and the fiddle,\nThe cow jumped over the moon.\nThe little dog laughed,\nTo see such sport,',
     'And the dish ran away with the spoon.']


def test_paras_list_input():
    assert paras(['Hey diddle diddle,',
                  '',
                  'The cat and the fiddle,',
                  'The cow jumped over the moon.',
                  'The little dog laughed,',
                  'To see such sport,',
                  '',
                  'And the dish ran away with the spoon.']) == \
        [['Hey diddle diddle,'],
         ['The cat and the fiddle,',
          'The cow jumped over the moon.',
          'The little dog laughed,',
          'To see such sport,'],
         ['And the dish ran away with the spoon.']]


def test_paras_with_comments():
    rhyme = """
        Hey diddle diddle,  # some comment!

        The cat and the fiddle,
        The cow jumped over the moon.
        The little dog laughed, # how he laughed!
        To see such sport,

        And the dish ran away with the spoon. # yee-ha!!
    """
    assert paras(rhyme) == \
    [['Hey diddle diddle,'],
     ['The cat and the fiddle,',
      'The cow jumped over the moon.',
      'The little dog laughed,',
      'To see such sport,'],
     ['And the dish ran away with the spoon.']]

    assert paras(rhyme, join="\n") == \
    ['Hey diddle diddle,',
     'The cat and the fiddle,\nThe cow jumped over the moon.\nThe little dog laughed,\nTo see such sport,',
     'And the dish ran away with the spoon.']

    assert paras(rhyme, cstrip=True) == paras(rhyme)

    assert paras(rhyme, cstrip=False) == \
    [['Hey diddle diddle,  # some comment!'],
     ['The cat and the fiddle,',
      'The cow jumped over the moon.',
      'The little dog laughed, # how he laughed!',
      'To see such sport,'],
     ['And the dish ran away with the spoon. # yee-ha!!']]

    assert paras(rhyme, cstrip=False, join="\n") == \
    ['Hey diddle diddle,  # some comment!',
    'The cat and the fiddle,\nThe cow jumped over the moon.\nThe little dog laughed, # how he laughed!\nTo see such sport,',
    'And the dish ran away with the spoon. # yee-ha!!']

    # NB comments on blank lines => they're no longer blank, unless cstrip=True
    # that can change entire shape of text paragraphization


def test_textline():
    assert textline("""
        this is
        a question
    """) == "this is a question"

    assert textline(["    this is", "    a question"]) == "this is a question"
