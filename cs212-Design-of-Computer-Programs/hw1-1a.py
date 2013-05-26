#!/usr/bin/env python
# -----------
# User Instructions
# 
# Write a function, allmax(iterable, key=None), that returns
# a list of all items equal to the max of the iterable, 
# according to the function specified by key. 

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    # Your code here.
    # from Norvig:
    #result, maxval = [], None
    key = key or (lambda x:x)
    #for x in iterable:
    #    xval = key(x)
    #    if not result or xval > maxval:
    #        result, maxval = [x], xval
    #    elif xval == maxval:
    #        result.append(x)
    #return result
    # if you don't make a new list, the iterable will be consumed to the end!
    #print mx
    #print hand_rank(mx)
    #print iterable
    #print [x for x in l]
    #print [x==mx for x in l]
    #print map(lambda x:(hand_rank(x)==hand_rank(mx)), iter(l))
    #print map(hand_rank, iter(l))
    L = list(iterable)
    # so now l holds the data and iterable is empty!
    import itertools
    mx = hand_rank(max(L, key=key))
    return list( itertools.ifilter(lambda x:hand_rank(x)==mx, iter(L) ) )

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
    "Return True if the ordered ranks form a 5-card straight."
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has exactly n-of-a-kind of.
    Return None if there is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    "If there are two pair here, return the two ranks of the two pairs, else None."
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None


mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC'] 

def deal(numhands, n=5, deck=mydeck):
    # Your code here.
    return [random.sample(deck,n*numhands)[(i*n):(i+1)*n] for i in range(numhands)]

def best_hand(hand):
    """
    Combinations works as long as the hand_rank function doesn't get confused by card order
    Perumtations inefficiently checks all possible 5-card hands to find the best one.
    """
    from itertools import combinations
    hands = [list(tp) for tp in combinations(hand,5)]
    # will this work with the tuple of tuples returned by itertools.combination() ?
    return allmax(hands) 
    

def test():
    "Test cases for the functions in poker program."
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2] 
    #print allmax(iter([['6C', '7C', '8C', '9C', 'TC'], ['6D', '7D', '8D', '9D', 'TD'], ['9D', '9H', '9S', '9C', '7D'], ['TD', 'TC', 'TH', '7C', '7D']]),hand_rank)
    assert allmax([['6C', '7C', '8C', '9C', 'TC'], ['6D', '7D', '8D', '9D', 'TD'], ['9D', '9H', '9S', '9C', '7D'], ['TD', 'TC', 'TH', '7C', '7D']],hand_rank) == [['6C', '7C', '8C', '9C', 'TC'],['6D', '7D', '8D', '9D', 'TD']]
    print best_hand("6C 7C 8C 9C TC 6D 7D".split())
    print best_hand("6C 7C 8C 9C TC 9D TD".split())
    print best_hand("6C 7C 8C 9C TC TD JD".split())
    print best_hand("6C 7C 8C 9C TC TD TS".split())
    print best_hand("6C 7C 9D 9C TC TD TS".split())
    return 'tests pass'

