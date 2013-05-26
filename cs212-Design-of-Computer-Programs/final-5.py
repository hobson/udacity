# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
    assert double_out(90) in (['DB', 'D20'],['T20','D15'])
    assert double_out(60) in (['D20', 'D10'],['T18', 'D3'])
    #return 'Passed test 1'
"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""

class hobson:
    "namespace for 'global' variables"
    # board geometry/order/scores definition
    ss    = '20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5'.split(' ')

    N = len(ss) # 20 for darts boards, number of sectors

    # create a dictionary for producing a score from every possible name
    s     = map(int,ss)
    score = [0   ]+ s                  +[i*2 for i in s    ]+[i*3 for i in s    ]
    name  = ['OFF']+['S%d'%i for i in s ]+['D%d'%i for i in s ]+['T%d'%i for i in s ]
    score += [25,50]
    name  += ['SB','DB']
    d     = dict(zip(name,score))
    #print s
    #print name
    #print score
    #print d

    # create a dictionary that outputs a name for every possible score
    s2    = range(1,21)
    score2= [0   ]+ s2                  +[i*2 for i in s2    ]+[i*3 for i in s2   ]
    name2 = ['OFF']+['S%d'%i for i in s2]+['D%d'%i for i in s2]+['T%d'%i for i in s2]
    # overwrite difficult ways to get same score (S last overwrites D's and T's,...)
    d2    = dict(zip(reversed(score2),reversed(name2)))
    d2[25]='SB'
    d2[50]='DB'
    #print s2
    #print name2
    #print score2
    #print d2

    # create a dictionary with just doubles
    score3= [i*2 for i in s2   ]
    name3 = ['D%d'%i for i in s2]
    # overwrite difficult ways to get same score (S last overwrites D's and T's,...)
    d3    = dict(zip(score3,name3))
    d3[50]='DB'
    #print d3

# from python 2.7 itertools
def combinations_with_replacement(iterable, r):
    # combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)

def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    bigfirst = list(hobson.score)
    bigfirst.sort(reverse=True)
    #print bigfirst
    # exhaustive search won't take long, so no need to optimize
    for i in range(3):
        for c in combinations_with_replacement(bigfirst,i+1):
            if sum(c)==total and c[-1]%2==0 and c[-1]/2 in hobson.s+[25]:
                result = [hobson.d2[target] for target in c]
                result[-1] = hobson.d3[c[-1]]
                return result
    return None

"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""

def outcome(target, miss):
    """Return a probability distribution of [(target, probability)] pairs.
    >>> outcome('S20', .2)
    {'D20': 0.016, 'S1': 0.096, 'T5': 0.002, 'S5': 0.096, 'T1': 0.002, 'S20': 0.768, 'T20': 0.016, 'D5': 0.002, 'D1': 0.002}
    """
    P = {}
    if target not in hobson.name or target == 'OFF':
        return {'OFF':1}
    ro = ring_outcome(target,miss)
    so = sector_outcome(target,miss)
    if target in ('DB','SB'):
        if target == 'DB':
            P[target]=so[target]*(1-ro['SB'])
            P['SB']  =so[target]*ro['SB']
        else:
            P[target]=so[target]*(1-ro['DB'])
            P['DB']  =so[target]*ro['DB']
        for k2,v2 in so.items():
            if k2 not in ('DB','SB'):
                P['S'+k2]=v2
    else:
        for k1,v1 in ro.items():
            for k2,v2 in so.items():
                if k1=='OFF':
                    P[k1] = v1*v2
                else:
                    P[k1+k2] = v1*v2
    return P

#Let me try to clarify a bit more. Some people in the discussion forum were confused about the miss ratio -- they missed the idea that there are two independent ways to miss, by ring and by section. One way to implement that is to have separate functions to return probability distributions for ring and section outcomes. For example, consider aiming for the S20 target with a miss ratio of 0.2. The S ring is the thick one, so the miss ratio is reduced to 1/5 * 0.2, and we would have:
def ring_outcome(target, miss):
    """
    >>> ring_outcome('S20', .2)
    {'S': 0.96, 'D': 0.02, 'T': 0.02}
    """
    SDT = target[0]
    if target[1] == 'B': # need to differentiate between SB and S
        SDT = target
    P = {SDT:1}
    if SDT == 'SB':
        P['DB'],P['S'] = miss/4,miss*3/4
    elif SDT == 'DB':
        P['SB'],P['S'] = miss,miss*2
        miss *= 3
    elif   SDT == 'T':
        P['S']   = miss
    elif SDT == 'D':
        P['S'],P['OFF'] = [miss/2]*2
    else:
        P['D'],P['T']   = [miss/10]*2
        miss /= 5
    P[SDT]   = 1-miss
    return P

def sector_outcome(target, miss):
    """
    >>> sector_outcome('S20', .2)
    {'1': 0.1, '20': 0.8, '5': 0.1}
    >>> sector_outcome('SB', .2)
    {'11': 0.01, '10': 0.01, '13': 0.01, '12': 0.01, '20': 0.01, '14': 0.01, '17': 0.01, '16': 0.01, '19': 0.01, '18': 0.01, 'SB': 0.8, '1': 0.01, '3': 0.01, '2': 0.01, '5': 0.01, '4': 0.01, '7': 0.01, '6': 0.01, '9': 0.01, '15': 0.01, '8': 0.01}
    >>> print len(sector_outcome('DB', .2))
    21
    """
    t = target[1:] if target[1:] != 'B' else target
    P = {}
    try:
        i = hobson.ss.index(t)
        P[hobson.ss[(i-1)%hobson.N]], P[hobson.ss[(i+1)%hobson.N]]  = [miss/2]*2 
    except:
        # assume everything but a valid sector is a bulls attempt
        for s0 in hobson.ss:
            P[s0]=miss/hobson.N
        # raise ValueError('Invalid target name specified')
    P[t]=1-miss
    return P

def outcome_score(oc):
    """
    >>> outcome_score(outcome('T20', 0.1)) 
    51.24
    
    # {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    # .81*60+.005*1+.045*15+.005*5+.045*3+.09*20
    """
    return sum([hobson.d[k]*v for k,v in oc.items()])

def best_target(miss):
    "Return the target that maximizes the expected score."
    best = 0.
    for n in hobson.name:
        #print n
        attempt = outcome_score(outcome(n,miss))
        #print attempt
        if attempt > best:
            best = attempt
            target = n
    return target
    
def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    #print outcome('T20', 0.1)

    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    #print 'ring'
    #print ring_outcome('SB',0.2)
    #print 'sector'
    #print sector_outcome('SB',0.2)
    #print 'total'
    #print outcome('SB', 0.2)
    assert same_outcome(
        outcome('SB', 0.2),
        {'S9': 0.01, 'S8': 0.01, 'S3': 0.01, 'S2': 0.01, 'S1': 0.01, 'DB': 0.04,
         'S6': 0.01, 'S5': 0.01, 'S4': 0.01, 'S19': 0.01, 'S18': 0.01, 'S13': 0.01,
         'S12': 0.01, 'S11': 0.01, 'S10': 0.01, 'S17': 0.01, 'S16': 0.01,
         'S15': 0.01, 'S14': 0.01, 'S7': 0.01, 'S20': 0.01, 'SB': 0.76})
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(
        outcome('SB', 0.2),
        {'S9': 0.01, 'S8': 0.01, 'S3': 0.01, 'S2': 0.01, 'S1': 0.01, 'DB': 0.04,
         'S6': 0.01, 'S5': 0.01, 'S4': 0.01, 'S19': 0.01, 'S18': 0.01, 'S13': 0.01,
         'S12': 0.01, 'S11': 0.01, 'S10': 0.01, 'S17': 0.01, 'S16': 0.01,
         'S15': 0.01, 'S14': 0.01, 'S7': 0.01, 'S20': 0.01, 'SB': 0.76})
    #return 'Passed test 2'
         

import doctest
doctest.testmod()
print test_darts()
print test_darts2()

