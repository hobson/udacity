#!/usr/bin/python
colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

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

def move_p(p, motion, p_move):
    pExact = p_move
    pUndershoot = 1-p_move
    pOvershoot = 0
    q=[]
    for i in range(len(p)):
        q.append([])
        for j in range(len(p[i])):
            q[i].append(0.)
            s = pExact * p[(i-motion[0]) % len(p)][(j-motion[1]) % len(p[i])]
            #s = s + pOvershoot * p[(i-motion[0]-1) % len(p)][(i-motion[1]-1) % len(p[i])]
            s = s + pUndershoot * p[i][j]
            q[i][j]=s
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
        p  = move_p(p,mot,p_move)
        p  = sense_p(p, measurements[i], colors, sensor_right)
    return p

p=compute_p(colors,measurements,motions,sensor_right,p_move)
#p_true = [[.011059, .0246404, .0679966, .0447248, .02465153],
#          [.00715,  .01017,   .086965,  .07988429,.00935066],
#          [.007397,.0089437,.11272,.353507,.0406555],
#          [.009106,.0071532,.01434,.04313329,.0364255]]
#for i in range(len(p_true)):
#    for j in range(len(p_true[i])):
#        print '{0:1.5f} '.format(p[i][j]-p_true[i][j])
#    print
#Your probability array must be printed 
#with the following code.

show(p)

#[0.011059807427972008, 0.02464041578496803, 0.067996628067859166, 0.044724870458121582, 0.024651531216653717] [0.0071532041833209815, 0.01017132648170589, 0.086965960026646888, 0.079884299659980826, 0.0093506685084371859] [0.0073973668861116709, 0.0089437306704527025, 0.11272964670259773, 0.3535072295521271, 0.040655492078276761] [0.0091065058056464965, 0.0071532041833209815, 0.014349221618346571, 0.043133291358448934, 0.036425599329004729]

