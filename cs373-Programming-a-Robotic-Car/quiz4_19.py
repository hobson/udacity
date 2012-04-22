#!/usr/bin/python2.6
"""
    >>> policy=optimum_policy()
    >>> for i in range(len(policy)):
    >>>     print policy[i]
    ['v', 'v', ' ', 'v', 'v', 'v']
    ['v', 'v', ' ', 'v', 'v', 'v']
    ['v', 'v', ' ', '>', '>', 'v']
    ['>', '>', '>', '^', ' ', 'v']
    ['^', '^', ' ', ' ', ' ', 'v']
    ['^', '^', '<', '<', ' ', '*']
"""
# ----------
# User Instructions:
# 
# Create a function optimum_policy() that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell.
# 
# un-navigable cells must contain an empty string
# WITH a space, as shown in the previous video.
# Don't forget to mark the goal with a '*'

# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

default_delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right


def optimum_policy(grid,delta=default_delta,delta_name=['^', '<', 'v', '>'],cost_step=1,init=[0,0],goal=[len(grid)-1, len(grid[0])-1]):
    value  = [[ 99 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True

    while change:
            change = False

            for x in range(len(grid)):
                for y in range(len(grid[0])):
                    if goal[0] == x and goal[1] == y:
                        if value[x][y] > 0:
                            value[x][y] = 0
                            change = True
                            policy[x][y] = '*'

                    elif grid[x][y] == 0:
                        for a in range(len(delta)):
                            x2 = x + delta[a][0]
                            y2 = y + delta[a][1]

                            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                                v2 = value[x2][y2] + cost_step

                                if v2 < value[x][y]:
                                    change       = True
                                    value[x][y]  = v2
                                    policy[x][y] = delta_name[a]

    return policy # Make sure your function returns the expected grid.

import pprint
pprint.pprint(optimum_policy(grid))

