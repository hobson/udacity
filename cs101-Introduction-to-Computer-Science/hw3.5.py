#!/usr/bin/python2.6

#Define a procedure, total_enrollment,
#that takes as an input a list of elements,
#where each element is a list containing
#three elements: a university name,
#the total number of students enrollect,
#and the annual tuition.

#The procedure should return two numbers,
#not a string,
#giving the total number of students
#enrolled at all of the universities
#in the list, and the total tuition
#(which is the sum of the number
#of students enrolled times the
#tuition for each university).

udacious_univs = [['Udacity',90000,0]]

usa_univs = [ ['California Institute of Technology',2175,37704],
              ['Harvard',19627,39849],
              ['Massachusetts Institute of Technology',10566,40732],
              ['Princeton',7802,37000],
              ['Rice',5879,35551],
              ['Stanford',19535,40569],
              ['Yale',11701,40500]  ]

#>>> print total_enrollment(udacious_univs)
#(90000,0)

#>>> print total_enrollment(usa_univs)
#(77285,3058581079L)

def total_enrollment(x):
    r = [0,0]
    for row in x:
        r[0] += row[1]
        r[1] += row[1]*row[2]
    return r

print total_enrollment(udacious_univs)
print total_enrollment(usa_univs)
    

