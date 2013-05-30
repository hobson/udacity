# Underscoring the Magnitude 
#
# Focus: Units 1 and 2, Regular Expressions and Lexical Analysis
#
# In this problem you will use regular expressions to specify tokens for a
# part of a new programming language. You must handle seven types of
# tokens:
#
#
#       PLUS            +
#       MINUS           -
#       TIMES           *
#       DIVIDE          /
#       IDENT           my_variable  Caps_Are_OK
#       STRING          'yes'  "also this"  
#       NUMBER          123  123_456_789
#
# The last three merit a more detailed explanation. 
#
# An IDENT token is a non-empty sequence of lower- and/or upper-case
# letters and underscores, but the first character cannot be an underscore.
# (Letters are a-z and A-Z only.) The value of an IDENT token is the string
# matched. 
#
# A STRING token is zero or more of any character surrounded by 'single
# quotes' or "double quotes". In this language, there are no escape
# sequences, so "this\" is a string containing five characters. The value
# of a STRING token is the string matched with the quotes removed.
#
# A NUMBER is a a non-empty sequence of digits (0-9) and/or underscores,
# except that the first character cannot be an underscore. Many real-world
# languages actually support this, to make large number easier to read.
# All NUMBERs in this language are positive integers; negative signs and/or
# periods are not part of NUMBERs. The value of a NUMBER is the integer
# value of its digits with all of the underscores removed: the value of
# "12_34" is 1234 (the integer).  
#
# For this problem we do *not* care about line number information. Only the
# types and values of tokens matter. Whitespace characters are ' \t\v\r'
# (and we have already filled them in for you below). 
#
# Complete the lexer below. 

import ply.lex as lex

tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
          'IDENT', 'STRING', 'NUMBER') 

#####
#

# Place your token definition rules here. 

#
#####

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_IDENT  = r'\w'
t_STRING  = r'([\'"]).*\1' # should I refer to the quote character to repeat it at the end?
# ERROR: Invalid regular expression for rule 't_STRING'. cannot refer to open group
#Traceback (most recent call last):
#  File "final-1.py", line 70, in <module>
#    lexer = lex.lex() 
#  File "/usr/lib/python2.7/dist-packages/ply/lex.py", line 901, in lex
#    raise SyntaxError("Can't build lexer")
#SyntaxError: Can't build lexer

#def t_string(t):
#  print "Lexer: unexpected character " + t.value[0]
#  t.lexer.skip(1) 



def t_error(t):
  print "Lexer: unexpected character " + t.value[0]
  t.lexer.skip(1) 

# We have included some testing code to help you check your work. Since
# this is the final exam, you will definitely want to add your own tests.
lexer = lex.lex() 

def test_lexer(input_string):
  lexer.input(input_string)
  result = [ ] 
  while True:
    tok = lexer.token()
    if not tok: break
    result = result + [(tok.type,tok.value)]
  return result

questions = []
question += " +   -   /   * " 
answer += [('PLUS', '+'), ('MINUS', '-'), ('DIVIDE', '/'), ('TIMES', '*')]

questions += """ 'string "nested" \' "inverse 'nested'" """
answer += [('STRING', 'string "nested" '), ('STRING', "inverse 'nested'")]

question += """ 12_34 5_6_7_8 0______1 1234 """
answer += [('NUMBER', 1234), ('NUMBER', 5678), ('NUMBER', 1), ('NUMBER', 1234)]

question += """ 'he'llo w0rld 33k """
answer += [('STRING', 'he'), ('IDENT', 'llo'), ('IDENT', 'w'), ('NUMBER',
0), ('IDENT', 'rld'), ('NUMBER', 33), ('IDENT', 'k')]

question += "'what is ' to 2+2 == 7\"?\"" 
answer += [('STRING', 'what is '), ('NUMBER', 2), ('PLUS', '+'), ('NUMBER', 2), ('EQUALS', '='), ('EQUALS', '='), ('NUMBER', 7), 'STRING',"?"]

for q in questions:
    print test_lexer(q) == a




