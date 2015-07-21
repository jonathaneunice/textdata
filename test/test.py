
from textdata import *
import sys

def _print(*args, **kwargs):
    """
    Python 2 and 3 compatible print function, similar to Python 3 arg handling.
    """
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    f   = kwargs.get('file', sys.stdout)
    parts = [str(item) for item in args ]
    parts.append(end)
    f.write(sep.join(parts))
    
    
def single_trial(name, t, **kwargs):
    _print("---", name, "---")
    reslines = lines(t, **kwargs)
    for line in reslines:
        _print(line)
    _print("--- end", name, "---")

    _print()
    
def test_basic():
    
    assert lines("""
                 a
                 line  
                 or
                 two""") == ['a','line','or','two']
    
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
    
def test_malindented_blank_lines():
    
    assert textlines(noblanks=False, text="""
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