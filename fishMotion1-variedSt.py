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
omegaT = [0, .25*math.pi, .5*math.pi, .75*math.pi, math.pi, 1.25*math.pi, 1.5*math.pi, 1.75*math.pi, 2*math.pi]

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

def dHdt(z,t):
    '''
        Finds Borazjani's dh/dt (eqivalent to Lighthill dz/dt)
    '''
    return (-omega*a(z)*math.sin(k*z-omega*t))

'''
    These help set initial time and z variables
'''
times = [0, 0.1, 0.2, 0.3, 0.5, 1, 2, 4, 9, 10, 20]
time = 1
# Makes list with values 0-1 with 1/clarity increments
clarity = 100
zVals = range(0,clarity)
zVals = [z/clarity for z in zVals]

'''
    The following lines were used to recreate the weird Borzjani wavy graph.
    All variables are in Borazjani coordinates
'''
# Makes list of u vals
# Note: these U-vals refer to Borazjani's forward velocity
numUVals = 6
UVals = range(-numUVals,numUVals)
UVals = [u/numUVals+.1 for u in UVals]

# Use list comprehension to get values of h
# The list comprehension seems to work, but I keep getting the same few values for multiple values of time
hVals = [[h(z, t) for z in zVals] for t in times]


# Try to use h2 function to vary omega
h2Vals = [[h2(z, time, omega1(u), k1(u)) for z in zVals] for u in UVals]
aVals = [a(z) for z in zVals]


'''
    Here, we tried to put Borazjani into Lighthill 
    I labeled Borzajani-based coordinates with a b afterwards, and 
    Lighthill-based coordinates with an l afterwards.
'''
# Determine (dh/dz)^2, then calculate the derivative of the arclength
dhdz2Vals = [dHdZ(z,time)**2 for z in zVals]
sPrime = [math.sqrt(1+dHdZ(z,time)**2) for z in zVals]

dz = L/clarity
print(dz)
sRects = [sP*dz for sP in sPrime]

# The following list comp produces a nearly linear fit...
arcLen = [sum(sRects[0:z]) for z in range(0,len(zVals))]

def estArc(z):
    '''
        Calculates the estimated arc length
        Note: doesn't work because z is not actually an index
        Just use the arcLen list comp above
    '''
    return sum(sRects[0:z*clarity])

# Let's try to findd the arclen using the above function
print (estArc(L))

# Find arclen at various times
def arcBasedOnTime(t):
    # Set up all the variables as before but name them differently
    # to avoid confusing Python
    clar = 100
    zV = range(0,clarity)
    zV = [z/clarity for z in zV]

    dhdz2 = [dHdZ(z,t)**2 for z in zV]
    sPrime = [math.sqrt(1+dHdZ(z,t)**2) for z in zV]

    dzb = L/clar
    sRects = [sP*dzb for sP in sPrime]

    # We want to find the arclength across the whole fish, so add everything
    return sum(sRects)

# Now make a list based off of times 
# note: omega is ~94. We need to vary omega*t between 0 and 2*pi.
# We find that 2*pi/94 = 0.66, so varying times between 0 and 0.66
# represents varied times over a period.
timesForArc = [0.66*t/clarity for t in range(0,100)]
arcsBasedtimes = [arcBasedOnTime(t) for t in timesForArc]
# All of the arclengths are about 1, which is what we should hope


'''
    General Notes from meetings bcs wow good organization:

    Finish find a-coord (arcLen)
    Xl = Zb
    Lighthill's dx/da = 1/sqrt(1+dhdz^2) = 1/sPrime
    dxl/dt is the forward velocity of the body (Use body len/sec = 1)
    dzl/dt is dh/dt
    To find dzl/da, we should find (dhb/dzb)/(dab/dzb)
'''
# Let's find dx/da and dz/da (Lighthill vars)
# Note: (dab/dzb) = da/dxl = sPrime
dxda = [1/sP for sP in sPrime]
dzda = [dHdZ(z,time)/math.sqrt(1+dHdZ(z,time)**2) for z in zVals]

# Test whether (dx/da)^2 + (dz/da)^2 = 1
tests = [dxa**2+dza**2 for (dxa,dza) in zip(dxda,dzda)]
# If you print tests, you'll see that the proposition is correct.
# Therefore, we can use the model

# Now, let's try to find the u and w vectors from Lighthill
# u = dx/dt*dx/da + dz/dt*dz/da
dzdt = [dHdt(z,time) for z in zVals]
uVec = [1*dxa + dzt*dza for (dxa,dzt,dza) in zip(dxda,dzdt,dzda)]
# w = dz/dt*dx/da - dx/dt*dz/da
wVec = [dzt*dxa - 1*dza for (dxa,dzt,dza) in zip(dxda,dzdt,dzda)]

#plt.plot(zVals, dzda)
plt.show()

# Next, we need to find momentum...


# Now let's try to find dzl/dal = dhb/dal
