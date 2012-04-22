#!/usr/bin/python

# N = original number of coconuts
# M = original number of men
M = 5
for N in range(1000000):
	Ni = N
	for m in range(M+1):
		if (Ni-1)%M != 0:
			done = False;
			break;
		else:
			Ni = (Ni-1)/M*4
			done = True
	if (m==M and Ni>0 and done):
		print 'the island had {0} coconuts'.format(N)
