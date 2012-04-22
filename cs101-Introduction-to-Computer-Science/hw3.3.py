#!/usr/bin/python2.6

def product_list(l):
    if len(l)<1:
        return None
    r = 1.
    for i in l:
        r *= i;
    return r
    
    
print product_list([9])
print product_list([1,2,3,4])
