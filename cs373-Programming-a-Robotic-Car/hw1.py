#!/usr/bin/python

# homework problem 1-1.1
Px = .2
Pnx = 1-Px
Pnx
print 'HW 1-1.1: Pnx =',Pnx

#cancer quiz problem, 1-32
Pc = 0.001
Pnc = 1-Pc
Pposgc = .8
Pposgnc = .1
Pcgpos_ = Pposgc*Pc
alpha = Pposgc*Pc + Pnc*Pposgnc
Pcgpos = Pcgpos_/alpha
print 'Quiz 1-32: Pcgpos =',Pcgpos

# homework problem 1-1.2
Px = .2
Py = .2
Pxandy = Px*Py
print 'HW 1-1.2: Pxandy =',Pxandy

# homework problem 1-1.3 values plugged into the cancer quiz 1-32
Px = .2
Pnx = 1-Px
Pygx = .6
Pygnx = .6
Pxgy_ = Pygx*Px
alpha = Pygx*Px+Pnx*Pygnx
Pxgy = Pxgy_/alpha
print 'HW 1-1.3 values in Quiz 1-32: Pxgy =',Pxgy

# homework problem 1-1.3
Py = Pygx*Px + Pygnx*Pnx
print 'HW 1-1.3: Py =',Py

# homework problem 1-2
N = range(1,7) # number of dimensions 1-6
M = 5 # number of cells in each dimension
mem = [M**N[i] for i in range(len(N))]
import math
print 'HW 1-2:          mem(1,2,...,N) =',mem
print 'HW 1-2:   quadratic:    mem/N^2 =',[mem[i]/math.sqrt(N[i]) for i in range(len(N))]
print 'HW 1-2: exponential: mem/exp(N) =',[mem[i]/(math.exp(N[i])) for i in range(len(N))]
print 'HW 1-2: exponential:    mem/M^N =',[mem[i]/(M**N[i]) for i in range(len(N))]

# homework problem 1-3
Pf = 0.001
Pnf = 1-Pf
Pbgf   = .9
Pnbgf  = .1
Pbgnf  = .1
Pnbgnf = .9
Pfgb_ = Pbgf*Pf
print 'HW 1-3.1:  Pfgb_ =',Pfgb_
Pnfgb_ = Pbgnf*Pnf
print 'HW 1-3.2: Pnfgb_ =',Pnfgb_
alpha = Pbgf*Pf + Pbgnf*Pnf
Pfgb = Pfgb_/alpha
print 'HW 1-3.3:   Pfgb =',Pfgb
Pnfgb = Pnfgb_/alpha
print 'HW 1-3.4:  Pnfgb =',Pnfgb

