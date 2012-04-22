#!/usr/bin/python2.6

def proc1(p):
    p[0]=p[1]

def proc2(p):
    p=p+[1]

def proc3(p):
    q=p
    p.append(3)
    q.pop() # surprisingly this undoes the change

def proc4(p):
    q=[]
    while p:
        q.append(p.pop())
    while q:
        p.append(q.pop())


x = [1,2,3]
proc1(x)
print x
x = [1,2,3]
proc2(x)
print x
x = [1,2,3]
proc3(x)
print x
x = [1,2,3]
proc4(x)
print x
