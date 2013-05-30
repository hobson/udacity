#!/usr/bin/env python
# module for solving the apartment "Floor" puzzle and measuring execution time

import itertools

def floor_puzzle():
    houses = bottom, _, _, _, top = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(houses)) # 1
    return next((Hopper, Kay, Liskov, Perlis, Ritchie) 
                for (Hopper, Kay, Liskov, Perlis, Ritchie) in orderings
                if (    Hopper is not top 
                    and Kay is not bottom
                    and Liskov is not top 
                    and Liskov is not bottom
                    and Perlis > Kay
                    and abs(Ritchie-Liskov) > 1
                    and abs(Liskov-Kay) > 1))

import time

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers)) 

def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time"""
    tt,times = 0,[]
    if isinstance(n,int):
        while tt < n:
            t,result = timedcall(fn,*args)
            times.append(t)
            tt += 1
    else:
        while tt < n:
            t, result = timedcall(fn,*args)
            tt += t
            times.append(t)
    return min(times), average(times), max(times)

print timedcall(floor_puzzle)
print timedcalls(1000,floor_puzzle)

