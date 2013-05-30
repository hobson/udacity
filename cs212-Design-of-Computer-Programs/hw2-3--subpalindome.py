#!/usr/bin/env python
# looks for a palindrome within a string
# _hobs version fails the efficiency check for 1 of the 4 answers/tests checked by Peter

# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    if not text: return (0,0)
    text=text.lower()
    candidate_slices = [ grow(text, i0, i1) for i0 in range(len(text))
                                            for i1 in (i0, i0+1)       ] # even and odd-lengthed pdromes
    print candidate_slices
    return max(candidate_slices, key=lambda s: s[1]-s[0])

def grow(text, i0, i1):
    """Grow length of slice indeces from center outward, checking palindrome symetry
    
    Start with 0 or 1-length strings"""
     # HL: what about starting at the first character (i0=0)? Single letter doesn't count as a palindrome? 
     # No, it's just that i0 isn't the first character in the checked palindrome--i0-1 is 
    while (i0 >0 and i1 < len(text) and text[i0-1].upper() == text[i1].upper() ):
        i0 -= 1; i1 += 1
    return (i0, i1)

def is_pal(text):
    if not text: return True
    for i in range(len(text)/2+1):
        if not text[i]==text[-1-i]: return False
    return True
    
test_examples="""racecar
Racecar
racecarX
Race carr
something rac e car going
xxxxx
Mad am I ma dam.
""".splitlines()

test_answers = [(0,7),(0,7),(0,7),(7,9),(8,21),(0,5),(0,15)]

def test():
    L = longest_subpalindrome_slice
    for t,a in zip(test_examples,test_answers):
        print t + ': ' + repr(L(t))
        assert L(t) == a
    print L('racecar')
    assert L('racecar') == (0, 7)
    print L('Racecar')
    assert L('Racecar') == (0, 7)
    
    print L('racecarX')
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()
