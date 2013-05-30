"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:



(You can assume that the days mentioned are all in the same week.)
"""

import itertools

def imafter(d1,d2):
    "Day1 is immediately after of Day2 if d1-d2 == 1."
    return d1-d2 == 1

def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    
    # Inventory of concepts: 
    names     = ['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes'] 
    N = len(names) # 5 people
    people    = (Hamming, Knuth, Minsky, Simon, Wilkes)  = list( range(1,N+1) ) # this is just an initial assignment
    # computers = laptop,  droid,    tablet,    iphone,  unspecified_computer = list( range(1,N+1) )
    # jobs      = manager, writer, designer, programmer, unspecified_job      = list( range(1,N+1) )
    days      = Mon, Tues, Wed, Thurs, Fri                                  = list ( range(1,N+1) ) # these are permanent
    
    orderings = list(itertools.permutations(people)) 
    order =    next( (Hamming, Knuth, Minsky, Simon, Wilkes) 
                for (Hamming, Knuth, Minsky, Simon, Wilkes)       in orderings
                #6. Knuth arrived the day after Simon.
                 if imafter(Knuth,Simon)
                for (manager, writer, designer, programmer, job) in orderings
                #4. The writer is not Minsky.
                 if writer is not Minsky
                #2. The programmer is not Wilkes.
                 if programmer is not Wilkes
                #10. Knuth arrived the day after the manager.
                 if imafter(Knuth,manager) # 10
                for (laptop, droid, tablet, iphone, other)        in orderings
                #3. Of the programmer and the person who bought the droid,
                #   one is Wilkes and the other is Hamming.
                #9. The designer didn't buy the droid.
                 if (programmer,droid) in [(Wilkes,Hamming),(Hamming,Wilkes)] and designer is not droid
                #1. The person who arrived on Wednesday bought the laptop.
                #12. Either the person who bought the iphone or the person who bought the tablet
                #    arrived on Tuesday.
                #11. Of the person who bought the laptop and Wilkes,
                #    one arrived on Monday and the other is the writer.
                #5. Neither Knuth nor the person who bought the tablet is the manager.
                #7. The person who arrived on Thursday is not the designer.
                #8. The person who arrived on Friday didn't buy the tablet.
                 if Wed is laptop and (iphone is Tues or tablet is Tues) and ((laptop,Wilkes) in [(Mon,writer),(writer,Mon)]) and Knuth is not manager and tablet is not manager and designer is not Thurs and Fri is not tablet
               )
#    print '(Hamming, Knuth, Minsky, Simon, Wilkes)'
#    print order
#    print '(laptop, droid, tablet, iphone, other)'
#    print order
#    print '(manager, writer, designer, programmer, job)'
#    print order
    return [dict(zip(order, names))[i] for i in range(1,N+1)]

print logic_puzzle()
