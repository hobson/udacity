#!/usr/bin/env python


def tricky_loop(p):
    i=0
    while True:
        i +=1
        if len(p) == 0:
            break
        else:
            #print 'len(p)',len(p)
            if p[-1] == 0:
                #print 'p[-1]',p[-1]
                p.pop() # assume pop is a constant time operation
            else:
                p[-1] = 0
                #print 'setting p[-1] to 0'
    return i
    
for N in range(100):
    p = [1.1*i for i in range(5,N+6)]
    print tricky_loop(p)

