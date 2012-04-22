#!/usr/bin/python2.6
#THREE GOLD STARS

#Sudoku [http://en.wikipedia.org/wiki/Sudoku]
#is a logic puzzle where a game
#is defined by a partially filled
#9 x 9 square of digits where each square
#contains one of the digits 1,2,3,4,5,6,7,8,9.
#For this question we will generalize
#and simplify the game.


#Define a procedure, check_sudoku,
#that takes as input a square list
#of lists representing an n x n
#sudoku puzzle solution and returns
#True if the input is a valid
#sudoku square and returns False
#otherwise.

#A valid sudoku square satisfies these
#two properties:

#   1. Each column of the square contains
#       each of the numbers from 1 to n exactly once.

#   2. Each row of the square contains each
#       of the numbers from 1 to n exactly once.

correct = [[1,2,3],
           [2,3,1],
           [3,1,2]]

incorrect = [[1,2,3,4],
             [2,3,1,3],
             [3,1,2,3],
             [4,4,4,4]]


def check_sudoku(s):
    N=len(s)
    M=len(s[0])
    if not N==M:
        return False
    validrows=[]
    validcols=[]
    for i in range(N):
        validrows.append(range(1,N+1))
        validcols.append(range(1,N+1))
    for i,row in enumerate(s):
        for j,el in enumerate(row):
            if el in validrows[i]:
                validrows[i].remove(el)
            else: 
                return False
            if el in validcols[j]:
                validcols[j].remove(el)
            else:
                return False
            #print validrows
            #print validcols
    for v in validrows:
        if not (len(v)==0):
            return False
    for v in validcols:
        if not (len(v)==0):
            return False
    return ((len(validrows)==N) and (len(validcols)==N))

#print check_sudoku(correct) == True
#print check_sudoku(incorrect) == False

