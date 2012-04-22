#!/usr/bin/env python

def explode_list(p,n):
    explosion = []
    for i in range(len(p)):
        explosion.extend([p[i]]*n)
    return explosion
    
assert(explode_list([1, 2, 3], 2) == [1, 1, 2, 2, 3, 3])

assert(explode_list([1, 0, 1], 0) == [])

assert(explode_list(["super","man"], 5) == ["super", "super", "super", "super", "super","man", "man", "man", "man", "man"] )

assert(explode_list(["super","man"], 0) == [] )
