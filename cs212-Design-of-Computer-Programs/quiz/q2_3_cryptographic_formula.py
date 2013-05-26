# -------------
# User Instructions
#
# Complete the fill_in(formula) function by adding your code to
# the two places marked with ?????. 

import string, re, itertools

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        #print f
        if valid(f):
            return f
    
def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = re.sub(r'[^A-Z]', '', formula)
    letters = ''.join(set(letters))
    for digits in itertools.permutations('1234567890', len(letters)):
        #print ''.join(digits), letters
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)
    
def valid(f):
    """Formula f is valid if and only if it has no 
    numbers with leading zero, and evals true."""
    try: 
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False