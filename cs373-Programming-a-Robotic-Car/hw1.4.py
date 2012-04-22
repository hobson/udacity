#!/usr/bin/python


motions = [	[[0,0]],
			[[0,0]],
			[[0,0]],
			[[0,0],[0,1]],
			[[0,0],[0,1]],
			[[0,0],[0,1]],
			[[0,0],[0,1],[1,0],[1,0],[0,1]],
		  ]
sensor_right=[1.,1.,.8,.8,.8,1.,.7]
p_move     = [1.,1.,1.,1.,.5,.5,.8]
colors = [	[['green','green','green'],['green','red','green'],['green','green','green']],
			[['green','green','green'],['green','red','red'],['green','green','green']],
			[['green','green','green'],['green','red','red'],['green','green','green']],
			[['green','green','green'],['green','red','red'],['green','green','green']],
			[['green','green','green'],['green','red','red'],['green','green','green']],
			[['green','green','green'],['green','red','red'],['green','green','green']],
			[['red','green','green','red','red'],['red','red','green','red','red'],['red','red','green','green','red'],['red','red','red','red','red']],
		 ]
measurements = [['red'],
				['red'],
				['red'],
				['red','red'],
				['red','red'],
				['red','red'],
				['green']*5,
			   ]
A = [	[[0.,0.,0.],[0.,1.,0.],[0.,0.,0.]],
		[[0.,0.,0.],[0.,.5,.5],[0.,0.,0.]],
		[[2./30]*3,[2./30,8./30,8./30],[2./30]*3],
		[[1./30]*3,[4./30,4./30,16./30],[1./30]*3],
		[[.0289855]*3,[.07246,.28985507,.4637681159],[.0289855]*3],
		[[0.]*3,[0.,1./3,2./3],[0.]*3],
		[[.01106,.02464,.0679966,.0447248,.02465],[.00715,.01017,.086965,.079884,.00935066],[.00739736,.00894,.11272,.3535,.0406],[.00911,.00715,.01435,.0431,.03642]],
	]

def printmat(mat):
	for row in mat:
		for el in row:
			print "{0:5.2f} ".format(el),
		print

def printmats(mats):
	for mat in mats:
		printmat(mat)

def printcharmat(mat):
	for row in mat:
		for el in row:
			print "{0!s:.1s} ".format(el),
		print

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
	#print '-'*80
	rows = len(colors)
	cols = len(colors[0])
	p_const = 1./(rows*cols)
	p=[]
	for i in range(rows):
		p.append([])
		for j in range(cols):
			p[i].append(p_const)
	
	printcharmat(colors)
	for i,mot in enumerate(motions): 
		p  = move_p(p,mot,p_move)
		p  = sense_p(p, measurements[i], colors, sensor_right)
	return p

num_ans = len(A);

errs=[]
for k in range(num_ans):
	rows = len(A[k])
	cols = len(A[k][0])
	errs.append([])
	for i in range(rows):
		errs[k].append([])
		for j in range(cols):
			errs[k][i].append(0.)

for k in range(num_ans):
	p = compute_p(colors[k],measurements[k],motions[k],sensor_right[k],p_move[k]);
	rows = len(A[k])
	cols = len(A[k][0])
	for i in range(rows):
		for j in range(cols):
			errs[k][i][j]=A[k][i][j]-p[i][j]
print'errs ='
printmats(errs)

colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

p=[]
p = compute_p(colors,measurements,motions,sensor_right,p_move)

def show(p):
    for i in range(len(p)):
        print p[i]
        
show(p)
