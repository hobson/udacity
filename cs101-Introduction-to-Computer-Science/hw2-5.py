import random

# 0 is neither positive nor negative, http://en.wikipedia.org/wiki/Integer

N=random.randint(1,1e7)


I=[]
I+=[0]
#I+=[[0,0,0]]
for N in range(1,int(1e7)):
	I+=[0]
#	I+=[[0,0,0]]
#	n=N
#	i = 0
#	while i <= n:
#		i = i+1
#	I[N][0]=i
#	#print 'loop 1 concluded with N={N:6d} \ti={i:6d} \tn={n:6d}'.format(N=N,i=i,n=n)

#	n=N
#	i = 1
#	while True:
#		i = i*2
#		n = n+1
#		if i > n:
#			break
#	I[N][1]=i
#	#print 'loop 2                N={N:6d} \ti={i:6d} \tn={n:6d}'.format(N=N,i=i,n=n)

	n=N
	i=1
	while n != 1:
		i+=1
		if n % 2 == 0: # n is even
		    n = n/2
		else:
		    n = 3*n + 1
#	I[N][0]=i
	I[N]=i
	if N%1000==0:
		print 'loop 3                N={N:6d} \ti={i:6d} \tn={n:6d}'.format(N=N,i=i,n=n)


