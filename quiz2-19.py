#!/usr/bin/python

def combine(mu1,var1,mu2,var2):
	mu = (var2*mu1+var1*mu2)/(var1+var2)
	var = 1./((1./var1)+(1./var2))
	return(mu,var)
	
(mu,var)=combine(10.,8.,13.,2.)
print (mu,var)
# homework 3-2
(mu,var)=combine(3.,1.,3.,1.)
print (mu,var)
