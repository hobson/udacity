# Unit 6: Fun with Words

"""
A portmanteau word is a blend of two or more words, like 'mathelete',
which comes from 'math' and 'athelete'.  You will write a function to
find the 'best' portmanteau word from a list of dictionary words.
Because 'portmanteau' is so easy to misspell, we will call our
function 'natalie' instead:

    natalie(['word', ...]) == 'portmanteauword'

In this exercise the rules are: a portmanteau must be composed of
three non-empty pieces, start+mid+end, where both start+mid and
mid+end are among the list of words passed in.  For example,
'adolescented' comes from 'adolescent' and 'scented', with
start+mid+end='adole'+'scent'+'ed'. A portmanteau must be composed
of two different words (not the same word twice).

That defines an allowable combination, but which is best? Intuitively,
a longer word is better, and a word is well-balanced if the mid is
about half the total length while start and end are about 1/4 each.
To make that specific, the score for a word w is the number of letters
in w minus the difference between the actual and ideal lengths of
start, mid, and end. (For the example word w='adole'+'scent'+'ed', the
start,mid,end lengths are 5,5,2 and the total length is 12.  The ideal
start,mid,end lengths are 12/4,12/2,12/4 = 3,6,3. So the final score
is

    12 - abs(5-3) - abs(5-6) - abs(2-3) = 8.

yielding a score of 12 - abs(5-(12/4)) - abs(5-(12/2)) -
abs(2-(12/4)) = 8.

The output of natalie(words) should be the best portmanteau, or None
if there is none. 

Note (1): I got the idea for this question from
Darius Bacon.  
Note (2): In real life, many portmanteaux omit letters,
for example 'smoke' + 'fog' = 'smog'; we aren't considering those.
Note (3): The word 'portmanteau' is itself a portmanteau; it comes
from the French "porter" (to carry) + "manteau" (cloak), and in
English meant "suitcase" in 1871 when Lewis Carroll used it in
'Through the Looking Glass' to mean two words packed into one. 
Note (4): the rules for 'best' are certainly subjective, and certainly
should depend on more things than just letter length.  In addition to
programming the solution described here, you are welcome to explore
your own definition of best, and use your own word lists to come up
with interesting new results.  Post your best ones in the discussion
forum. 
Note (5) The test examples will involve no more than a dozen or so
input words. But you could implement a method that is efficient with a
larger list of words.
"""

# Inventory of concepts:
# words         = a list of words provided as input
# ordered_pairs = a list of pairs of words [(w0,w1),(w0,w2),...] where w0,...,wN =words
# package       = w0[:N0] + (w0[N0:N1] or w1[N0:N1]) + w1[N1:]
# N0 in range(1,len(w1)) # have to leave at least one letter for beginning and another for middle
# N1 in range(1,len(w2))

import itertools
def score(N,N0,N1):
    """number of letters w minus the difference between the actual and ideal lengths of start, mid, and end
       N  = number index value returned by find_overlaps (mid length)
       N1 = len(w1)
       N2 = len(w2)"""
    if N<0: # signals a word order swap
        N,N0,N1=-N,N1,N0
    #print N0-N,N,N1-N
    Ntot = N0+N1-N
    #print .25*Ntot,.5*Ntot,.25*Ntot
    # TODO: simplify algebra...
    return Ntot-abs(0.25*Ntot-max(N0-N,0))-abs(0.5*Ntot-N)-abs(0.25*Ntot-max(N1-N,0)) 
    
def scores(Ns,pair):
    """Ns  = list of index value returned by find_overlaps (which is len(mid))
       w1 = pair[0] = the 1st word
       w2 = pair[2] = the 2nd word"""
    N0 = len(pair[0])
    N1 = len(pair[1])
    return [(score(abs(N),N0,N1),N) for N in Ns] # TODO: simplify algebra


def find_overlaps(pair):
    """List of integer indeces for the locations of all possible overlaps between one word and another, in either direction. 
    Negative means flipped word order."""
    w1,w2=pair
    N1,N2=len(w1),len(w2)
    N = min(N1,N2)-1
#    print N,N1,N2
    if N>0:
        overlaps = []
        for i in range(1,N+1):
            if w1[-i:]==w2[:i]:
                overlaps.append(i)
            if w2[-i:]==w1[:i]:
                overlaps.append(-i)
    return overlaps

def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."
    ports = dict()
    port = None
    maxs = 0
    for pair in itertools.combinations(words,2):
        Ns = find_overlaps(pair)
        s = max(scores(Ns,pair) or ((0,0),(0,0)) ) 
        N=s[1]
        if N<0:
            N,w1,w2 = -N,pair[1],pair[0]
        else:
            N,w1,w2 =  N,pair[0],pair[1]
        if s[0]>maxs:
            port = w1+w2[N:]
            maxs = s[0]
    return port

def test_natalie():
    "Some test cases for natalie"
    #print natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) 
    assert natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) in ('adolescented','adolescentennial')
    assert natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese']) == 'eskimono'
    assert natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage']) == 'kimcheese'
    assert natalie(['circus', 'elephant', 'lion', 'opera', 'phantom']) == 'elephantom'
    assert natalie(['programmer', 'coder', 'partying', 'merrymaking']) == 'programmerrymaking'
    assert natalie(['int', 'intimate', 'hinter', 'hint', 'winter']) == 'hintimate'
    assert natalie(['morass', 'moral', 'assassination']) == 'morassassination'
    assert natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) in ('entrepreneuropsychologist', 'entrepreneurotoxin')
    assert natalie(['perspicacity', 'cityslicker', 'capability', 'capable']) == 'perspicacityslicker'
    assert natalie(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog']) == 'backgroundhog'
    assert natalie(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops']) == 'nudisturbance'
    assert natalie(['night', 'day']) == None
    assert natalie(['dog', 'dogs']) == None
    assert natalie(['test']) == None
    assert natalie(['']) ==  None
    assert natalie(['ABC', '123']) == None
    assert natalie([]) == None
    return 'tests pass'


print test_natalie()



