#!/usr/bin/python2.6

def greatest(l):
    r = None
    if len(l)<1.:
        return 0
    for i in l:
        if i>r:
            r=i
    return float(r)
    
    
print greatest([9])
print greatest([-1,-2,-3,-4])
print greatest([4,23,1])
print greatest([])
