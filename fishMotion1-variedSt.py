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

# Constants for the function a
a0 = 0.02
a1 = -0.08
a2 = 0.16
amax = 0.1


# Constants for dimensionless parameters
f = 1
hmax = amax*L




'''
    RELEVANT FUNCTIONS
'''
def a(z):
    '''
        First Fourier Coefficient describing the amplitude envelop of lateral motion
    '''
    return (a0 + a1*z +a2*(z**2))

def dAdZ(z):
    return (a1+2*a2*z)

def h(z, t):
    '''
        Represents the lateral excursion of the fish at time t
    '''
    return a(z)*math.sin(k*z-omega*t)

def h2(z, t, ome1, k1):
    '''
        Another variation of h for debugging. I ended up giving up...
    '''
    return a(z)*math.sin(k1*z-ome1*t)
    #I'm just going to try all of this on 
    
def omega1(u):
    '''
        Calculates a new omega depending on U
    '''
    St = 2*f*hmax/u
    return math.pi*St/amax

def k1(u):
    '''
        Calculates a new k depending on U
    '''
    return 2*math.pi/(dimLam*1)

def dHdZ(z, t):
    '''
        Finds Borijani's dh/dz at a given z and t
    '''
    return (dAdZ(z)*math.sin(k*z-omega*t) +a(z)*k*math.cos(k*z-omega*t))


times = [0, 0.1, 0.2, 0.3, 0.5, 1, 2, 4, 9, 10, 20]
time = 1
# Makes list with values 0-1 with 1/clarity increments
clarity = 100
zVals = range(0,clarity)
zVals = [z/clarity for z in zVals]

# Makes list of u vals
numUVals = 6
uVals = range(-numUVals,numUVals)
uVals = [u/numUVals+.1 for u in uVals]

# Use list comprehension to get values of h
# The list comprehension seems to work, but I keep getting the same few values for multiple values of time
hVals = [[h(z, t) for z in zVals] for t in times]


# Try to use h2 function to vary omega
h2Vals = [[h2(z, time, omega1(u), k1(u)) for z in zVals] for u in uVals]
aVals = [a(z) for z in zVals]

# Determine (dh/dz)^2, then calculate the derivative of the arclength
dhdz2Vals = [dHdZ(z,time)**2 for z in zVals]
sPrime = [math.sqrt(1+dHdZ(z,time)**2) for z in zVals]

dz = L/clarity
print(dz)
sRects = [sP*dz for sP in sPrime]
arcLen = [sum(sRects[0:z]) for z in range(0,len(sRects))]

def estArc(z):
    '''
        Calculates the estimated arc length 
    '''
    return sum(sRects[0:z*clarity])



plt.plot(zVals, arcLen)
plt.show()

# plt.plot(zVals,hVals[1],zVals,hVals[3])
# print(len(hVals[0]))
# plt.plot(zVals,hVals[1])
# print(len(hVals[1]))
# plt.plot(zVals,hVals[2])
# print(len(hVals[2]))
# plt.plot(zVals,hVals[3])
# print(len(hVals[3]))

'''
    Finish find a-coord (arcLen)
    Xl = Zb
    Lighthill's dx/da = sqrt(1+dhdz^2)
'''

# Show the plot