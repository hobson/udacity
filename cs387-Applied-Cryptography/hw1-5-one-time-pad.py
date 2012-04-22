#!/usr/bin/env python

import random
Y = bin(ord('Y'))[2:]
N = bin(ord('N'))[2:]


K = bin(random.randint(0,127))[2:]
M = Y if random.randint(0,1) else N

def xor(s1,s2):
	"""
	Computes the exclusive or, XOR, or two strings of 1's and zeros.
	
	Returns a string of ones and zeros
	>>> xor('1100','0101')
	'1001'
	"""
	# bin() function returns a string that starts with 0b
	if s1.find('0b')==0:
		s1=s1[2:]
	if s2.find('0b')==0:
		s2=s2[2:]
	N = max(len(s1),len(s2))
	s1=zeropad(s1,N)
	s2=zeropad(s2,N)
	result = '' #'-'*N
	for i,c1 in enumerate(s1):
		result += str((int(c1)+int(s2[i]))%2)
	return result

def zeropad(s,N=7,prepend=True):
	pad = '0'*(N-len(s))
	return (pad+s if prepend else s+pad)

C = xor(M,K)
print 'C',C

Cy = xor(Y,K)
Cn = xor(N,K)

print 'Y',Y
print 'N',N



