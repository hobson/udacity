Pe = .13
Pa = .08
Po = Pi = .07
Pu = .03

Pv = Pe+Pa+Po+Pi+Pu
print 'Pv',Pv
# see http://stackoverflow.com/questions/4273695/ipython-automatically-echo-result-of-assignment-statement

Pna = 1-Pa
print 'Pna',Pna

# intersection (AND) of Pv and Pna
Pvana = Pv - (1-Pna) # NOT Pv*Pna
print 'Pvana',Pvana
Pvana = Pv - Pa
print 'Pvana',Pvana
Pvana = Pna - (1-Pv)
print 'Pvana',Pvana

Pvgna = Pvana/Pna
print "Def of Cond Prob: Pvgna",Pvgna

Pnagv = (Pv-Pa)/Pv
Pvgna = Pv/Pna * Pnagv
print "Baye's Rule: Pvgna",Pvgna
print 'But must truncate, not round, to 2 digits, per instructor comments.'





