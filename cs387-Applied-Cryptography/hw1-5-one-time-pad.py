#!/usr/bin/env python

import random
Y = bin(ord('Y'))[2:]
N = bin(ord('N'))[2:]
nlY = chr(eval('0b'+Y))
nlN = chr(eval('0b'+N))
print chr(eval('0b'+Y)),Y
print chr(eval('0b'+N)),N


K = bin(random.randint(0,127))[2:]
M = Y if random.randint(0,1) else N
C = '1001110'







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

print "so Alice's key is either",xor(Y,C),'or',xor(N,C)
print "If Alice sent Y then the key was",xor(Y,C),'so Mallory would send',xor(N,xor(Y,C))
print "If Alice sent N then the key was",xor(N,C),'so Mallory would send',xor(Y,xor(N,C))
print "If they are the same then Mallory has won!"

xC = xor(M,K)
print 'example C',xC
print 'intercepted C',C

Cy = xor(Y,K)
print 'E(Y)',Cy
Cn = xor(N,K)
print 'E(N)',Cn

spoofY = xor(C,Y)
print 'Y-spoofed/flipped message',spoofY
spoofN = xor(C,N)
print 'N-spoofed/flipped message',spoofN
spoofYN = xor(xor(C,Y),N)
print 'YN-spoofed/flipped message',spoofYN
spoofNY = xor(xor(C,N),Y)
print 'YN-spoofed/flipped message',spoofNY

print 'spoofing "key"', xor(Y,N)

Msy = xor(spoofY,K)
print "Bob's decryption",Msy,chr(eval('0b'+Msy))
Msn = xor(spoofN,K)
print "Bob's decryption",Msn,chr(eval('0b'+Msn))
Msyn = xor(spoofYN,K)
print "Bob's decryption",Msyn,chr(eval('0b'+Msyn))
Msny = xor(spoofNY,K)
print "Bob's decryption",Msny,chr(eval('0b'+Msny))


