#!/usr/bin/env python
"""
>>> [[0.5714285714285714,0.14285714285714285],[0,0]]
colors = [['g', 'g'],
          ['r', 'g']]
measurements = ['r',0]
motions = [[0,0],[-1,0]]
"""

colors = [['g', 'g'],
          ['r', 'g']]

measurements = ['r']

motions = [[-1,0]] # [row (down) motion , column (right) motion]

sensor_error = .2
sensor_right = 1-sensor_error

p_move = 1.0

def show(p):
    for i in range(len(p)):
        print p[i]

p = []
def normalize_p(p):
    s=0.
    for row in p:
        s+=sum(row) 
    if s>0.:
        for row,p_row in enumerate(p):
            for col,p_col in enumerate(p_row):
                p[row][col] /= s
    return p

def sense_p(p, meas, world, sense_right):
    q=[]
    for i in range(len(p)):
        q.append([])
        for j in range(len(p[i])):
            q[i].append(0.)
            hit = (meas == world[i][j])
            q[i][j] = (p[i][j] * (hit * sense_right + (1-hit) * (1-sense_right)))
    q = normalize_p(q)
    return q

def move_p(p, motion, p_move, wraparound=False):
    rows = len(colors)
    if wraparound:
        minrow = -inf # allow infinite wrap-around past the top
        maxrow = +inf # allow infinite wrap-around past the bottom
        mincol = [-inf for i in range(rows)] # allow infinite wrap-around past the left side
        maxcol = [+inf for i in range(rows)] # allow infinite wrap-around past the right side
    else:
        minrow = 0 # impassible barrier
        maxrow = rows-1 # impassible barrier
        mincol = [0 for i in range(rows)] # impassible barrier, one for each row on the left side
        maxcol = [max(len(p[0])-1,0) for i in range(rows)] # impassible barrier, one for each row on the right side
    print minrow
    print maxrow
    print mincol
    print maxcol
    pExact = p_move
    pUndershoot = 1-p_move
    pOvershoot = 0
    q=[] # probability matrix after a move
    for i in range(rows):
        q.append([])
        for j in range(len(p[i])):
            q[i].append(0.)
            # len(p[i]) and min/maxcol[i] allows variable-length (variable-width) rows
            # modulo function allows wrap-around by setting min/max row/col outside of the width/height of the map/matrix
            if motion[0]>
            s = pExact * p[min(max(i-motion[0],minrow),maxrow) % rows][min(max(j-motion[1],mincol[i]),maxcol[i]) % len(p[i])]
            #s = s + pOvershoot * p[(i-motion[0]-1) % len(p)][(i-motion[1]-1) % len(p[i])]
            s = s + pUndershoot * p[i][j]
            q[i][j]=s
    #q = normalize_p(q)
    return q

def compute_p(colors,measurements,motions,sensor_right,p_move):
    rows = len(colors)
    cols = len(colors[0])
    p_const = 1./(rows*cols)
    p=[]
    for i in range(rows):
        p.append([])
        for j in range(cols):
            p[i].append(p_const)
    for i,mot in enumerate(motions): 
        if mot:
            p  = move_p(p,mot,p_move)
        if measurements[i]
            p  = sense_p(p, measurements[i], colors, sensor_right)
    return p
p=compute_p(colors,measurements,motions,sensor_right,p_move)
#Your probability array must be printed 
#with the following code.

show(p)


