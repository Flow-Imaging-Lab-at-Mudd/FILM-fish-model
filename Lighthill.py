'''
    This file takes the formulas from the lighthill mathematica notebook and puts them into 
    Python 3
'''

import math
import matplotlib.pyplot as plt

'''
    RELEVANT CONSTANTS
'''

# Present in the Mathematica File, not sure why
rho = 1
s = 1
l = 1

# Wave Parameters
# Note: I'm not really sure where half these constants come from
dimLam = 0.95
L = 1
k = 2*math.pi/(dimLam*1)
omega = 2*math.pi*0.3/(2*.01)


# a goes from 0 to L
numAVals = 20
a = range(0,numAVals)
a = [aVal/numAVals+.0001 for aVal in a]

time = range(0,numAVals)
time = [2/(t+0.00000001) for t in time]

# Define x and z at time t
t = 0.5

def xPos(a, t):
    return a*t

def zPos(a, t):
    return t*t+a*a

x = [xPos(a, t) for aVal in a]
z = [zPos(a,t) for aVal in a]


# Calculate analytic derivatives?
h = 0.01

dxda = [[(xPos(a-h,t)-xPos(a,t))/h for aVal in a] for t in times]
dzda = [[(zPos(a-h,t)-zPos(a,t))/h for aVal in a] for t in times]
dxdt = [[(xPos(a,t-h)-xPos(a,t))/h for aVal in a] for t in times]
dzdt = [[(zPos(a,t-h)-zPos(a,t))/h for aVal in a] for t in times]

plt.plot(x, z)
plt.show()


