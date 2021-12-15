# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 18:25:03 2021

@author: Gianluca
"""

# Packages

import numpy as np
from numpy.linalg import inv
from matplotlib import pyplot as plt


def F(t):
    F = np.array([0.0,0.0])
    if t < 15.0 :
        F[0] = F0 * np.cos(omega*t)
    else: 
        F[0] = 0.0
    return F

def G(y,t):
    return inv(A).dot( F(t) - B.dot(y))
        

# Runge-Kutta 4th order
def RK4_step(y,t,dt):
    k1 = G(y,t)
    k2 = G(y+0.5*k1*dt, t+0.5*dt)
    k3 = G(y+0.5*k2*dt, t+0.5*dt)
    k4 = G(y+k3*dt, t+dt)
    
    #return dt*G(y,t)
    return dt* (k1 +2*k2 + 2*k3 + k4)/6


# Variables

m = 2
k = 2
c = 0.3

F0 = 1.0
delta_t = 0.1 
omega = 1.0
time = np.arange(0.0, 60.0, delta_t) #time vector



# inital state
y = np.array([0,1]) # [velocity, displacement]

A = np.array([[m,0],[0,1]])
B = np.array([[c,k],[-1,0]])
#C = np.array([[1,0],[0,1]])



Y = [] # memory of position
force = []


# time-stepping solution (Euler method)

for t in time:
    
        
    y = y + RK4_step(y,t,delta_t)
    
    Y.append(y[1])
    force.append(F(t)[0])
    
   
    KE = 0.5 * m * y[0]**2 # kinetic energy
    PE = 0.5 * k * y[1]**2 # potential energy
    if t%1 <= 0:
        print('Total energy:', KE+PE)
    
    
# plot the result
plt.plot(time,Y)
plt.plot(time,force)
plt.grid(True)
plt.legend(['Displacement','Force'], loc ='lower right')
plt.show    
    
    
    
    
    
    
    
    