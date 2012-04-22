#!/usr/bin/python2.6

def test(x):
    if x>0.:
        return True
    return False

def proc(a,b):
    if test(a):
        return b
    return a

def proc1(x,y):
    if test(x):
        return y
    else:
        return x

def proc2(a,b):
    if not test(b):
        return a
    else:
        return b

def proc3(a,b):
    result = a
    if test(a):
        result = b
    return result

def proc4(a,b):
    if not test(a):
        b = 'udacity'
    else:
        return b
    return a

A = [-.1,0,1.9]
B = [-.1,0,1.9]

Aa =  [[0,0,0],[0,0,0],[0,0,0]]
Aa1 = [[0,0,0],[0,0,0],[0,0,0]]
Aa2 = [[0,0,0],[0,0,0],[0,0,0]]
Aa3 = [[0,0,0],[0,0,0],[0,0,0]] 
Aa4 = [[0,0,0],[0,0,0],[0,0,0]]
e1 = [[0,0,0],[0,0,0],[0,0,0]]
e2 = [[0,0,0],[0,0,0],[0,0,0]]
e3 = [[0,0,0],[0,0,0],[0,0,0]]
e4 = [[0,0,0],[0,0,0],[0,0,0]]

for i,a in enumerate(A):
    for j,b in enumerate(B):
        Aa[i][j] = proc(a,b)
        Aa1[i][j] = proc1(a,b)
        Aa2[i][j] = proc2(a,b)
        Aa3[i][j] = proc3(a,b)
        Aa4[i][j] = proc4(a,b)
        e1[i][j] = (Aa[i][j] == Aa1[i][j])
        e2[i][j] = (Aa[i][j] == Aa2[i][j])
        e3[i][j] = (Aa[i][j] == Aa3[i][j])
        e4[i][j] = (Aa[i][j] == Aa4[i][j])
        

print 'proc1'
print e1
print 'proc2'
print e2
print 'proc3'
print e3
print 'proc4'
print e4
