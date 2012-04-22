#!/usr/bin/env python

Pfair = .5
Punfair = .6
Pchoose = .5

print 'probability of choosing fair and getting 2 heads:'
print Pchoose*Pfair*Pfair
print 'probability of choosing unfair and getting 2 heads:'
print (1-Pchoose)*Punfair*Punfair

print 'probability of getting 2 heads either way'
P_twoheads = Pchoose*Pfair*Pfair + (1-Pchoose)*Punfair*Punfair
print P_twoheads

P_twoheads_g_unfair = Punfair*Punfair
print 'P_twoheads_g_unfair=',P_twoheads_g_unfair

P_unfair = (1-Pchoose)
print 'P_unfair=',P_unfair

# Bayes Rule
# P_AgB = P_BgA * P_A / P_B 

P_unfair_g_twoheads = P_twoheads_g_unfair * P_unfair / P_twoheads
print 'P_unfair_g_twoheads=',P_unfair_g_twoheads
 
