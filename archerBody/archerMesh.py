# Script to manipulate the archer fish body mesh .stl file
# ToDo: Convert to iPython
import numpy as np
import trimesh
import matplotlib.pyplot as plt

# Read in .stl files of body without fins and body with median fins
fishy = trimesh.load_mesh('archerfish_rescaled_finless.stl')
fishyfin = trimesh.load_mesh('archerfish_rescaled_median.stl')
#fishy.show()
#fishyfin.show()
wt = fishy.is_watertight

len = abs(fishy.bounds[0,2]-fishy.bounds[1,2])
lenfin = abs(fishyfin.bounds[0,2]-fishyfin.bounds[1,2])
print str(len)+' is fish body length'
print str(lenfin)+' is length with fins'

# shift origin to y centroid
cent = fishy.center_mass
shift = np.copy(cent)
#shift[0]=0
shift[2]=fishy.bounds[0,2]

fishy.vertices -= shift
fishyfin.vertices -= shift

# 2d projection for added mass estimate (large-amplitude EBT style?)
# create slices along length of fish
nlev=180
zlevels_ends = np.linspace(fishy.bounds[0,2],fishy.bounds[1,2],nlev+2)

# trim extremal levels to prevent code crashes
zlevels = zlevels_ends[1:-1];

dz = zlevels[1]-zlevels[0];

# sections array
sections = [None]*(nlev)
areas = np.zeros(nlev)
centx = np.zeros(nlev)
centy = np.zeros(nlev)
yL = np.zeros(nlev)
yU = np.zeros(nlev)

yshift = np.zeros(nlev)

for i, z in enumerate(zlevels):
    #section at each z location
    slice3d = fishy.section(plane_origin = [0,0,z],plane_normal = [0,0,1])
    yL[i]=(slice3d.bounds[0,1])
    yU[i]=(slice3d.bounds[1,1])

    sections[i],to_3D=slice3d.to_planar()

    yshift[i]=to_3D[1,3]

    #enclosed area of each section
    areas[i]=sections[i].area

    pgon = sections[i].polygons_full
    centx[i]=(pgon[0].centroid.x)
    centy[i]=(pgon[0].centroid.y)+yshift[i]

# get local width of body in cm (not mm)    
localwidth = (yU-yL)/10

# use 1/4*pi*rho*s^2 for virtual mass per length (Lighthill)
# using rho = 1 g/cm^3
m_per_len = .25*np.pi*np.square(localwidth)
# units of m_per_len are g/cm

# write mass per length to file
#print zlevels.shape
#print m_per_len.shape

#reshape z levels (now also in cm) and mass per length to array
writedata = np.array([zlevels/10,m_per_len])

# output file
outfile = 'added_mass_per_length.txt'
hdr = 'Y'+'\t'+'m'
f = open(outfile,'wb')
f.write(bytes(hdr+'\n'))
f.close()
f = open(outfile,'ab')
np.savetxt(f, writedata.T, fmt='%10.5f', delimiter='\t')
f.close()

plt.subplot(2,2,1)
plt.plot(zlevels,areas)
plt.xlabel('Z (mm)')
plt.ylabel('x-sect area')

#volume distribution
Vol = np.cumsum(areas*dz)
Vsub = fishy.volume - Vol
Psub = Vsub/fishy.volume*100

plt.subplot(2,2,2)
plt.plot(zlevels,Vol)
plt.plot((fishy.bounds[0,2],fishy.bounds[1,2]),(fishy.volume,fishy.volume))
plt.plot(zlevels,Vsub)
plt.xlabel('Z (mm)')
plt.ylabel('Volume (mm3)')

plt.subplot(2,2,3)
plt.plot(zlevels,yL)
plt.plot(zlevels,yU)
plt.plot(zlevels,centy)
plt.plot(zlevels,m_per_len)
plt.xlabel('Z (mm)')
plt.ylabel('Y (mm)')

#test determining centroid of submerged portion
xtest = np.average(centx, weights=areas)
ytest = np.average(centy, weights=areas)
ztest = np.average(zlevels, weights=areas)

#loop to determine Center of Buoyancy
xsub = np.zeros(nlev-1)
ysub = np.zeros(nlev-1)
zsub = np.zeros(nlev-1)

for i in range (0,nlev-1):
    xsub[i] = np.average(centx[i+1:], weights=areas[i+1:])
    ysub[i] = np.average(centy[i+1:], weights=areas[i+1:])
    zsub[i] = np.average(zlevels[i+1:], weights=areas[i+1:])

cmdist = zsub - fishy.center_mass[2]

plt.subplot(2,2,4)
plt.plot(zlevels[1:],xsub)
plt.plot(zlevels[1:],ysub)
plt.plot(zlevels[1:],cmdist)
plt.xlabel('Last underwater point')
plt.ylabel('Center of buoyancy')

plt.show()                      
