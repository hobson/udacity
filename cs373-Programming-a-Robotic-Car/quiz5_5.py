#!/usr/bin/python2.6

# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth)
# and returns a smooth path.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the previous video:
#
# If your function isn't submitting it is possible that the
# runtime is too long. Try sacrificing accuracy for speed.
# -----------

from math import *

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

# ------------------------------------------------
# smooth coordinates
#

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = .00000001):

    # Make a deep copy of path into newpath
    newpath = [[0 for row in range(len(path[0]))] for col in range(len(path))]
    for i in range(len(path)):
        for j in range(len(path[0])):
            newpath[i][j] = path[i][j]


    #### ENTER CODE BELOW THIS LINE ###
    changes = tolerance
    while changes >= tolerance:
        changes = 0.0
        for i in range(1,len(newpath)-1): # should check for 1-length paths
            # iterate over dimensions of path to smooth
            # this should be outside the tolerance loop to allow each dimension to terminate independently
            # but Thrun did it inside, so that affects the answer
            for d in range(len(path[0])):
                oldpath = newpath[i][d]
                # should sum the two changes before altering newpath, but that's not what Thrun did
                newpath[i][d] += weight_data  *(   path[i][d]   - newpath[i][d])
                # why not just pick the middle point between the neighboring points and go straight there?
                # this creates a "delta" that is twice as far as what is needed
                # So the weighting for smoothing should be half as large as what your intuition would expect (i.e. 0.5 is the max)
                # By being sloppy about the derivation and implementation of the smoother, the weights lose any meaning
                #   It just becomse a matter of playing with the weights to get the path that you want and hoping it's good enough
                # No way to PROVE that your path will meet any particular performance metrics for efficiency or smoothness, 
                #   or proximity to found path from search results
                newpath[i][d] += weight_smooth*(newpath[i-1][d] + newpath[i+1][d] - 2*newpath[i][d]) 
                changes += abs(oldpath-newpath[i][d])
    return newpath # Leave this line for the grader!

# feel free to leave this and the following lines if you want to print.
newpath = smooth(path)

# thank you - EnTerr - for posting this on our discussion forum
for i in range(len(path)):
    print '['+ ', '.join('%.3f'%x for x in path[i]) +'] -> ['+ ', '.join('%.3f'%x for x in newpath[i]) +']'
    # [[0,1],[0.029 0.971]...]






