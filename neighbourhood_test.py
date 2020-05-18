# -*- coding: utf-8 -*-
"""
Created on Mon May 18 11:00:33 2020

@author: Hal

NEIGHBOURHOOD TEST

place particles all over the place
search the neighbourhood given point
(highlight in matplotlib)
time

(c o n s i d e r  b o u n d a r y  s a m p l i n g ?)
"""
import numpy as np
import numpy.linalg
import random
import matplotlib.pyplot as plt
import time

class Particle:
    def __init__(self,pos):
        self.pos = pos
        
#PARAMETERS:
h = 0.1 #kernel smoothing radius/support radius (not the same in general, but equal for cubic spline)

Nx = 0,1 #dim
Ny = 0,1 #dim

N = 10000 #number of particles

#SET UP PARTICLES
particle_list = []
for n in range(N):
        pos = np.array( [random.uniform(Nx[0],Nx[1]) , random.uniform(Ny[0],Ny[1])] )
        particle_list.append(Particle(pos))

t0 = time.time()

#NEIGHBOURHOOD PREPROCESSING
bins = {}
rows = int( (Ny[1]-Ny[0])//h )
cols = int( (Nx[1]-Nx[0])//h )

for i in range(-1,rows+2): #we go +/-1 to allow for empty "outside" boxes and avoid throwing key errors
    for j in range(-1,cols+2):
        bins[(i,j)] = []
for p in particle_list:
    gx, gy = p.pos[0]//h , p.pos[1]//h
    bins[(gx,gy)].append(p)

#LOOKUP
#choose target for testing
target = random.choice(particle_list)        

#find neighbours of target:
GX, GY = target.pos[0]//h, target.pos[1]//h
considered = []
for dx in range(-1,2):
    for dy in range(-1,2):
        considered += bins[(GX+dx,GY+dy)]

neighbours =[]
for c in considered:
    if np.linalg.norm(c.pos-target.pos) <= h:
        neighbours.append(c)

tf = time.time()-t0    
print("Time taken for ",N," points: ",round(tf,4)," seconds")
##plot
xneigh=[]
yneigh=[]
for n in neighbours:
    xneigh.append(n.pos[0])
    yneigh.append(n.pos[1])

xcons = []
ycons = []
for c in considered:
    xcons.append(c.pos[0])
    ycons.append(c.pos[1])
    
xdat = []
ydat = []
for p in particle_list:
    xdat.append(p.pos[0])
    ydat.append(p.pos[1])
    
radius_display = plt.Circle( target.pos, h, color="r", fill=False)

fig, ax = plt.subplots()

ax.add_artist(radius_display)
ax.scatter(xdat,ydat)
ax.scatter(xcons,ycons,color="g")
ax.scatter(xneigh,yneigh,color="r")
ax.scatter(target.pos[0],target.pos[1],color="b")

ax.set_aspect(1)
xgrid = [i*h for i in range(cols+2)]
ygrid = [i*h for i in range(rows+2)]
ax.set_xticks(xgrid)
ax.set_yticks(ygrid)
ax.grid(which='both')