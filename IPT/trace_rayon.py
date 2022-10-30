#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 19:41:23 2022

@author: theofauvet
"""

import matplotlib.pyplot as plt
import numpy as np

import trace_surface as ts
import trace_plan_tangent as tpt

def rayon_incident(theta_0,d,x_repos,y_repos,option=1): # d = distance entre le miroir et l'écran
    if option == 1:
        ask = input("Tracer le rayon incident ?")
    else :
        ask = 'n'
    abscisse_liste = np.linspace(-d,d,100)
    x_ray = [x_repos - al for al in abscisse_liste]
    y_ray = [y_repos for al in abscisse_liste]
    z_ray = [xp/np.tan(theta_0) for xp in abscisse_liste]
    if ask == 'y':
        plt.plot(x_ray,y_ray,z_ray)
    return(x_ray,y_ray,z_ray)

def intersection(x,y,z,theta_0,d,x_repos,y_repos,option=1):
    if option == 1:
        ask = input("Tracer l'intersection membrane/rayon réfléchi?")
    else :
        ask = 'n'
    x_ray,y_ray,z_ray = rayon_incident(theta_0,d,x_repos,y_repos,option=0)
    a,b = z.shape
    for i in range(a):
        for j in range(b):
            for k in range(len(x_ray)):
                if abs(x[i,j]-x_ray[k])<0.02:
                    if abs(y[i,j]- y_repos) <0.02:
                        if abs(z[i,j]-z_ray[k]) < 0.02:
                            if option == 1:
                                if ask == 'y':
                                    plt.plot(x[i,j],y[i,j],z[i,j],'ro')
                            return(i,j)
                                            
def calcul_angle(X,Y,Z,x,y,z,theta_0,d,i,j):
    theta_1x = np.arctan((Z[2,0]-z[i,j])/(X[2,0]-x[i,j]))
    theta_1y = np.arctan((Z[0,1]-z[i,j])/(Y[0,1]-y[i,j]))
    return(theta_1x,theta_1y)
    
def rayon_reflechie(X,Y,Z,x,y,z,theta_0,d,i,j,x_repos,y_repos,option=1):
    if option == 1:
        ask = input("Tracer le rayon réfléchi ?")
    else :
        ask = 'n'
    theta_x,theta_y = calcul_angle(X,Y,Z,x,y,z,theta_0,d,i,j)
    abscisse_liste = np.linspace(-d,d,100)
    x_ray = [x[i,j] + al for al in abscisse_liste]
    y_ray = [y[i,j]-np.tan(theta_y)*x[i,j] + np.tan(theta_y)*xp for xp in x_ray] 
    z_ray = [z[i,j] + np.tan(theta_x - theta_0 + np.pi/2)*al for al in abscisse_liste] 
    if ask == 'y':
        plt.plot(x_ray,y_ray,z_ray)
    return(x_ray,y_ray,z_ray)
    
def projection_ecran(X,Y,Z,x,y,z,theta_0,d,x_repos,y_repos,i,j,option=1):
    if option == 1:
        ask = input("Tracer le point sur l'écran ?")
    else :
        ask = 'n'
    theta_x,theta_y = calcul_angle(X,Y,Z,x,y,z,theta_0,d,i,j)
    print(theta_x,theta_y)
    H_y = np.tan(theta_y)*d + y[i,j]-np.tan(theta_y)*x[i,j]
    H_z = np.tan(theta_x - theta_0 + np.pi/2)*d + z[i,j]  
    if ask == 'y':
        plt.plot(d,H_y,H_z,'bo')
    return(H_y,H_z)

def plot_ecran(theta_0,d,temps,a,c,modes,x_repos,y_repos,fig,ax):
    ask = input('Tracer points sur écran ?')
    H = [[],[]] # Coordonnées sur l'écran
    for t in temps:
        r,theta,x,y,z_membrane = ts.trace_membrane(a,c,modes,t,fig,ax,option=0)
        x_ray_inc,y_ray_inc,z_ray_inc = rayon_incident(theta_0,d,x_repos,y_repos,option=0)
        i,j = intersection(x,y,z_membrane,theta_0,d,x_repos,y_repos,option=0)
        X,Y,Z_plan = tpt.plan_tangent(r,theta,x,y,z_membrane,i,j,fig,ax,option=0)
        H[0].append(projection_ecran(X,Y,Z_plan,x,y,z_membrane,theta_0,d,x_repos,y_repos,i,j,option=0)[0])
        H[1].append(projection_ecran(X,Y,Z_plan,x,y,z_membrane,theta_0,d,x_repos,y_repos,i,j,option=0)[1])
    if ask == 'y':
        plt.figure()
        plt.plot(H[0],H[1])
        plt.grid()
        plt.show()
    return(H)
        
