import aima.probability as p

T=True
F=False

sprinkler = p.BayesNet([
    p.node('Cloudy', '', 0.5),
    p.node('Sprinkler', 'Cloudy', {T: 0.10, F: 0.50}),
    p.node('Rain', 'Cloudy', {T: 0.80, F: 0.20}),
    p.node('WetGrass', 'Sprinkler Rain',
         {(T, T): 0.99, (T, F): 0.90, (F, T): 0.90, (F, F): 0.00})])
    
hw2_6 = p.BayesNet([
    p.node('A', '', 0.65),
    p.node('C', '', 0.45),
    p.node('B', 'A', {T: 0.10, F: 0.80}),
    p.node('D', 'A C', {(T,T): 0.10, (T,F): 0.50, (F,T): .40, (F,F): .1}),
    p.node('E', 'A B D', {(T,T,T): 0.70, (T,T,F): 0.30, (T,F,T): .60, (T,F,F): .05,
                        (F,T,T): 0.25, (F,T,F): 0.45, (F,F,T): .55, (F,F,F): .15})])

numfmt = '%.9g'
a1=p.enumeration_ask('A',{'B':True}, hw2_6).show_approx(numfmt)
a2=p.enumeration_ask('A',{'B':True,'C':True}, hw2_6).show_approx(numfmt)
a3=p.enumeration_ask('A',{'B':True,'C':False}, hw2_6).show_approx(numfmt)

hw2_6 = p.BayesNet([
    p.node('A', '', 0.65),
    p.node('C', '', 0.95), # changed just this value to see if it ripples through to answer
    p.node('B', 'A', {T: 0.10, F: 0.80}),
    p.node('D', 'A C', {(T,T): 0.10, (T,F): 0.50, (F,T): .40, (F,F): .1}),
    p.node('E', 'A B D', {(T,T,T): 0.70, (T,T,F): 0.30, (T,F,T): .60, (T,F,F): .05,
                        (F,T,T): 0.25, (F,T,F): 0.45, (F,F,T): .55, (F,F,F): .15})])

a4=p.enumeration_ask('A',{'B':True}, hw2_6).show_approx(numfmt)

# these all come out the same
print a1
print a2
print a3
print a4

