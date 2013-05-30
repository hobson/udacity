def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key = len)
        return text[:len(text)-len(shortest)]

def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text) or 1):
        m = match(pattern, text[i:])
        if m is not None: return m

def lit(s): return lambda t: set([t[len(s):]]) if t.startswith(s) else null
def seq(x, y): return lambda t: set().union(*map(y, x(t)))
def alt(x, y): return lambda t: x(t) | y(t)
def oneof(chars): return lambda t: set([t[1:]]) if (t and t[0] in chars) else null
def opt(x): return lambda t: alt(lit(''), x)(t)

dot = lambda t: set([t[1:]]) if t else null
eol = lambda t: set(['']) if t == '' else null
def star(x): return lambda t: (set([t]) |
                               set(t2 for t1 in x(t) if t1 != t
                                   for t2 in star(x)(t1)))
def plus(x): return lambda t: seq(x, star(x))(t)

null = frozenset([])

def test():
    g = alt(lit('a'), lit('b'))
    assert g('abc') == set(['bc'])

    assert match(star(lit('a')), 'aaaaabbbaa') == 'aaaaa'
    assert match(lit('hello'), 'hello how are you?') == 'hello'
    assert match(lit('x'), 'hello how are you?') == None
    assert match(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
    assert match(oneof('xyz'), '   x is here!') == None

    assert match(star(lit('a')), 'aaabcd') == 'aaa'
    assert match(lit('abc'), 'abc') == 'abc'
    assert match(alt(lit('b'), lit('c')), 'ab') == None
    assert match(alt(lit('b'), lit('a')), 'ab') == 'a'
    assert search(lit(''), '') == ''
    assert search(alt(lit('b'), lit('c')), 'ab') == 'b'
    assert search(star(alt(lit('a'), lit('b'))), 'ab') == 'ab'
    assert search(alt(lit('b'), lit('c')), 'ad') == None
    assert lit('abc')('abcdef') == set(['def'])
    assert (seq(lit('hi '), lit('there '))('hi there nice to meet you')
            == set(['nice to meet you']))
    assert alt(lit('dog'), lit('cat'))('dog and cat') == set([' and cat'])
    assert dot('am i missing something?') == set(['m i missing something?'])
    assert dot('') == frozenset([])
    assert oneof('a')('aabc123') == set(['abc123'])
    assert oneof('abc')('babc123') == set(['abc123'])
    assert oneof('abc')('dabc123') == frozenset([])
    assert eol('') == set([''])
    assert eol('not end of line') == frozenset([])
    assert star(lit('hey'))('heyhey!') == set(['!', 'heyhey!', 'hey!'])
    assert plus(lit('hey'))('heyhey!') == set(['!', 'hey!'])
    assert opt(lit('hey'))('heyhey!') == set(['hey!', 'heyhey!'])

    return 'tests pass'

print test()
