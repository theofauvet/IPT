#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:00:34 2022

@author: theofauvet
"""

############################# RESET LES VARIABLES
from IPython import get_ipython
def __reset__(): get_ipython().magic('reset -sf')

__reset__()
#############################

import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D 

import trace_surface as ts
import trace_plan_tangent as tpt
import trace_rayon as tr

a = 1 # rayon de la membrane 
modes = (0,1) # Définition des mode(s) de la membrane
c = 0.75 # Vitesse des ondes
x_repos,y_repos = 0.25,0.25 # Point que l'on étudie
t = 1  # Instant étudié
theta_0 = np.pi/4 # Angle d'incidence
d = 1 # Distance miroir écran

fig = plt.figure() # Ouverture d'une figure
ax = fig.add_subplot(111, projection='3d') # Définition des axes 
ax.autoscale(False)

r,theta,x,y,z = ts.trace_membrane(a,c,modes,t,fig,ax) # Tracé de la membrane
x_ray_inc,y_ray_inc,z_ray_inc = tr.rayon_incident(theta_0,d,x_repos,y_repos) # Tracé du rayon incident
i,j = tr.intersection(x,y,z,theta_0,d,x_repos,y_repos) # Point d'intersection entre le rayon incident et la membrane à l'instant t
X,Y,Z = tpt.plan_tangent(r,theta,x,y,z,i,j,fig,ax) # Tracé du plan tangent
x_ray_ref,y_ray_ref,z_ray_ref = tr.rayon_reflechie(X,Y,Z,x,y,z,theta_0,d,i,j,x_repos,y_repos) # Tracé du rayon réfléchie
H_x,H_y = tr.projection_ecran(X,Y,Z,x,y,z,theta_0,d,x_repos,y_repos,i,j)

# temps = np.linspace(0,10,100)
# H = tr.plot_ecran(theta_0,d,temps,a,c,modes,x_repos,y_repos,fig,ax)







