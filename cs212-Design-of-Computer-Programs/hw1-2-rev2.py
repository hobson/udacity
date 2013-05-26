# CS 212, hw1-2: Jokers Wild
#
# -----------------
# User Instructions
#
# Write a function best_wild_hand(hand) that takes as
# input a 7-card hand and returns the best 5 card hand.
# In this problem, it is possible for a hand to include
# jokers. Jokers will be treated as 'wild cards' which
# can take any rank or suit of the same color. The 
# black joker, '?B', can be used as any spade or club
# and the red joker, '?R', can be used as any heart 
# or diamond.
#
# The itertools library may be helpful. Feel free to 
# define multiple functions if it helps you solve the
# problem. 
#
# -----------------
# Grading Notes
# 
# Muliple correct answers will be accepted in cases 
# where the best hand is ambiguous (for example, if 
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

import itertools



def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."

    # Your code here
    hands = [list(tp) for tp in itertools.combinations(hand,5)]
    # Must deal with more than one best hand (ties), but may only happen in 10-choose-5 hands
    return allmax(hands,key=hand_rank)[0]



# ------------------
# Provided Functions
# 
# You may want to use some of the functions which
# you have already defined in the unit to write 
# your best_hand function.

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand) 
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)
    
def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered 
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has 
    exactly n-of-a-kind of. Return None if there 
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two 
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None 

def allmax(iterable, key=None):
    key = key or (lambda x:x)
    L = list(iterable)
    # so now l holds the data and iterable is empty!
    import itertools
    mx = hand_rank(max(L, key=key))
    #print mx
    return list( itertools.ifilter(lambda x:hand_rank(x)==mx, iter(L) ) )

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    ranks = '23456789TJQKA'
    blk = [r+'C' for r in ranks] + [r+'S' for r in ranks]
    red = [r+'H' for r in ranks] + [r+'D' for r in ranks]
    # Your code here
    hib = hand.index('?B')+1 if '?B' in hand else None
    
    hands = [list(tp) for tp in itertools.combinations(hand,5)]
    #brute force
    morehands=[]
    
    #import pprint
    #pprint.pprint(hands)
    #print '----------------------------------------------'
    #print
    #pprint.pprint(morehands)
    
    # this can be functionalized
    for i,hand in enumerate(hands):
        hib = hand.index('?B')+1 if '?B' in hand else None
        #print hib
        if hib:
            # this can be list-comprehended
            for r in ranks:
                #print r
                for s in 'CS':
                    card = r+s
                    if card not in hand: # don't let the wild card duplicate an existing card (not sure if this is a rule)
                    #print s
                        hand[hib-1] = card
                    #print hand
                    morehands.append(list(hand)) # be sure to create a new list each time
                    #print morehands
        else:
            morehands.append(hand)
            #print morehands
    
    hands = morehands
    #pprint.pprint(morehands)
    #return allmax(morehands, key=hand_rank)[0]
    #print '===================================='
    morehands=[]
    
    #pprint.pprint(hands)
    #print '----------------------------------------------'
    #print
    #pprint.pprint(morehands)
    
    # this can be functionalized
    for i,hand in enumerate(hands):
        hir = hand.index('?R')+1 if '?R' in hand else None
        if hir:
            # this can be list-comprehended
            for r in ranks:
                for s in 'HD':
                    card = r+s
                    if card not in hand:
                        hand[hir-1] = card
                    morehands.append(list(hand)) # be sure to create a new list each time
        else:
            morehands.append(hand)
    
    #pprint.pprint(hands)
    #pprint.pprint(morehands)
    #print '----------------------------------------------'
    #print
    
    return allmax(morehands, key=hand_rank)[0]

def test_best_wild_hand():
    #print sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    #print sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    print sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    return 'test_best_wild_hand passes'

print test_best_wild_hand()
