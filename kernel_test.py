# -*- coding: utf-8 -*-
"""
Created on Sat May 16 03:25:17 2020

@author: Hal
"""
import numpy as np
import math 
import matplotlib.pyplot as plt
import random

class Particle:
    def __init__(self,x,y):
        self.mass = 18 #kg
        self.neighbour_list = set([])
        self.pos = np.array((x,y))


def main():
    #currently set up to span from y = 0,1.5, x = -2,+2
    Nx , Ny = 4,1.5
    global h,normalisation
    h = 0.6
    normalisation = 40/(7*math.pi*(h**2)) #2D normalisation factor
    spacing = h/2 #suitable heuristic (a.k.a. particle diameter)
    display_string = "Spacing = " + str(spacing) +"\nSmoothing = " + str(h) + "\n Norm = "+str(round(normalisation,3))
    print(display_string)
    particle_list, grid_hash = populate_list(Nx,Ny,spacing)
    print(len(particle_list)," particles generated.")
    test_along_parameter(particle_list,display_string)
    return particle_list

def test_along_parameter(particle_list, display_string):
    fig, axs = plt.subplots(2)
    xdat,ydat = [],[]
    for p in particle_list:
        xdat.append(p.pos[0])
        ydat.append(p.pos[1])
    axs[1].scatter(xdat,ydat)
    axs[1].set_title("System diagram")
    
    for func, col in (  (trig_func,"r"),(quad_func,"b"),(step_func,"g")):
        xtdat, ytdat = eval_function(particle_list, func, axs, col)
    
    #plt.text(S, 0.8, display_string, horizontalalignment='right', verticalalignment='center')
    axs[0].set_title("Parameter Sampling Result")
    axs[1].plot(xtdat,ytdat,color="r")
    print("ok")
    plt.tight_layout()
    return

def eval_function(particle_list, func,axs,col):
    print(col)
    sdata = []
    realdata = []
    approxdata = []
    S=100
    xtdat, ytdat = [],[]
    for s in range(S):
        tx, ty = parameterize(s/S)
        xtdat.append(tx)
        ytdat.append(ty)
        sdata.append(s/S)
        realdata.append(func( (tx,ty) ))
        approxdata.append(discretisation_approx(tx,ty,particle_list,func))
    axs[0].plot(sdata,realdata,color=col)
    axs[0].plot(sdata,approxdata,color=col,linestyle='dashed')
    return xtdat, ytdat

def parameterize(s):
    #simple linear: x = 0.1s, y = 0.1s
    x = -2 + 4*s
    y = 3*(x+2)/8
    return x,y

def populate_list(Nx,Ny,pspacing):
    pspacing = pspacing/2
    fuzz = 0.02
    p_list = []
    grid_hash = {}
    nx = int(Nx//pspacing)
    ny = int(Ny//pspacing)
    for i in range(nx):
        for j in range(ny):
            newx = (i*pspacing-2 ) + random.uniform(-fuzz,fuzz)
            newy =  j*pspacing + random.uniform(-fuzz,fuzz)
            item = Particle(newx,newy)
            p_list.append(item)   
            # I,J = int(i//spacing), int(j//spacing)
            # grid_hash[I,J].append(item)
            
    return p_list, grid_hash

def quad_func(pos):
    x = pos[0]
    y = pos[1]
    return (x**2 + y**2)*0.5 - 1
    
def trig_func(pos):
    x = pos[0]
    y = pos[1]
    return -2*math.sin(2*x)

def step_func(pos):
    x = pos[0]
    if x < 0:
        return -2
    else:
        return +2
    
def discretisation_approx(x,y,particle_list,func):
    res = 0
    
    for particle in particle_list:
        rho = density((x,y),particle_list)
        res += func(particle.pos)*particle.mass*kernel_function((x,y),particle.pos)/rho
    return res

def density(pos,particle_list):
    res = 0.01
    for j in particle_list:
        res += j.mass * kernel_function(pos,j.pos)
    return res

def kernel_function(xi, xj):
    global h
    #cubic spline kernel
    norm = 2*40/(7*math.pi*(h**2)) #2D normalisation factor
    #norm = 4/(3*h)
    q = dist_sq(xi,xj) / h   
    if 0 <= q <= 0.5:
        W = norm*(6*(q**3 - q**2) + 1)
    elif 0.5 < q <= 1:
        W = norm*2*(1-q)**3
    else:
        W = 0
    return W

def dist_sq(a,b):
    xdist = a[0] - b[0]
    ydist = a[1] - b[1]
    return xdist**2 + ydist**2

def get_neighbourhood(particle,particle_list):
    #terrible, crude placeholder
    global h
    threshold = 2*h #???
    particle.neighbour_list = set([])
    for j in particle_list:
        if dist_sq(particle,j) < threshold:
            particle.neighbour_list |= j
            
A = main()