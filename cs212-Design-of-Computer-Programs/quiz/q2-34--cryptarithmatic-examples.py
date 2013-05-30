#!/usr/bin/env python
# solves any cryptarithmatic problem using brute force

# --------------
# User Instructions
# 
# Modify the function compile_formula so that the function 
# it returns, f, does not allow numbers where the first digit
# is zero. So if the formula contained YOU, f would return 
# False anytime that Y was 0 

from __future__ import division
import re, itertools, string, time

def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as parms of function. The first digit of a multi-digit 
    number can't be 0. So if YOU is a word in the formula, and the function
    is called with Y eqal to 0, the function should return False."""
    
    # modify the code in this function.
    
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    firstletters = set(re.findall(r'\b([A-Z])[A-Z]', formula))
    parms = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)
    if firstletters:
        tests = ' and '.join(L+'!=0' for L in firstletters)
        body = tests+' and ('+body+')'
    f = 'lambda %s: %s' % (parms, body)
    if verbose: print f
    return eval(f), letters

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words uncahanged: compile_word('+') => '+'"""
    if word.isupper():
        terms = [('%s*%s' % (10**i, d)) 
                 for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word
    
def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass
            
def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers)) 
    
def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    tt,times = 0,[]
    if isinstance(n,int):
        while tt < n:
            t,result = timedcall(fn,*args)
            times.append(t)
            tt += 1
    else:
        while tt < n:
            t, result = timedcall(fn,*args)
            tt += t
            times.append(t)
    return min(times), average(times), max(times)

examples = """TWO+TWO==FOUR
A**2+B**2==C**2
A**2+BE**2==BY**2
X/X==X
A**N+B**N==C**N and N>1
A**N+B**N==C**N and N>2
AB**N+C**N==EF**N and N>2
AB**N+CD**N==EF**N and N>2
AB**N+CD**N==EFG**N and N>2
AB**N+CD**N==EFGH**N and N>2
ATOM**.5 == A + TO + M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < THREE
RAMN == R**3 + RM**3 == N**3 + RX**3
sum(range(AA)) == BB
sum(range(POP))== BOBO
ODD+ODD==EVEN
PLUTO not in set([PLANETS])""".splitlines()

# Peter Norvig suggested he'd be interested if we could solve the problem A**3+B**3==C**3
# Seems to me you can use an anaalogy
#   for 2-D (**2) problem, you can divide a square into a set of equally-sized squares
#   
def test():
    t0 = time.clock()
    for e in examples:
        print; print 13*' ', e
        print '%6.4f sec:  %s ' % timedcall(faster_solve, e)
    print '%6.4f tot.' % (time.clock()-t0)
    
    assert faster_solve('A + B == BA') == None # should NOT return '1 + 0 == 01'
    assert faster_solve('YOU == ME**2') == ('289 == 17**2' or '576 == 24**2' or '841 == 29**2')
    assert faster_solve('X / X == X') == '1 / 1 == 1'
    return 'tests pass'

test()
