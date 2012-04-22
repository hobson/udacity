#!/usr/bin/python2.6

p = [1, 0, 1]
p[0] = p[0]+p[1]
p[1]=p[0]+p[2]
p[2]=p[0]+p[1]
print p == [1,2,3]
