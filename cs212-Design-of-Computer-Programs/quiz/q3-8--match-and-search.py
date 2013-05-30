#---------------
# User Instructions
#
# Complete the search and match functions. Match should
# match a pattern only at the start of the text. Search
# should match anywhere in the text.

def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:
            return m
        
def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = matchset(pattern, text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]
    
def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y

def matchset(pattern, text):
    "Match pattern at start of text; return a set of remainders of text."
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y, text)
    elif 'dot' == op:
        return set([text[1:]]) if text else null
    elif 'oneof' == op:
        return set([text[1:]]) if text.startswith(x) else null
    elif 'eol' == op:
        return set(['']) if text == '' else null
    elif 'star' == op:
        return (set([text]) |
                set(t2 for t1 in matchset(x, text)
                    for t2 in matchset(pattern, t1) if t1 != text))
    else:
        raise ValueError('unknown pattern: %s' % pattern)
    
null = frozenset()

def lit(string):  return ('lit', string)
def seq(x, y):    return ('seq', x, y)
def alt(x, y):    return ('alt', x, y)
def star(x):     return ('star', x)
def plus(x):      return seq(x, start(x))
def opt(x):       return alt(lit(''), x)
def oneof(chars): return ('oneof', tuple(chars))
dot = ('dot',)
eol = ('eol',)

def test():
    assert match(('star', ('lit', 'a')),'aaabcd') == 'aaa'
    assert match(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == None
    assert match(('alt', ('lit', 'b'), ('lit', 'a')), 'ab') == 'a'
    assert search(('alt', ('lit', 'b'), ('lit', 'c')), 'ab') == 'b'
    return 'tests pass'

print test()
