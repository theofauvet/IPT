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
import polynomial_regression as pr

def rayon_incident(theta_0,d_inc,x_repos,y_repos,option=1): # d = distance entre le miroir et l'écran
    if option == 1:
        ask = 'y'
    else :
        ask = 'n'
    abscisse_liste = np.linspace(-d_inc,d_inc,100)
    x_ray = [x_repos - al for al in abscisse_liste]
    y_ray = [y_repos for al in abscisse_liste]
    z_ray = [xp/np.tan(theta_0) for xp in abscisse_liste]
    if ask == 'y':
        plt.plot(x_ray,y_ray,z_ray)
    return(x_ray,y_ray,z_ray)

def intersection(x,y,z,theta_0,d_inc,x_repos,y_repos,option=1):
    if option == 1:
        ask = 'y'
    else :
        ask = 'n'
    x_ray,y_ray,z_ray = rayon_incident(theta_0,d_inc,x_repos,y_repos,option=0)
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

def find_sym(pt,line_pt,line_vec):
    pt_proj = np.dot(pt - line_pt, line_vec) * line_vec / np.dot(line_vec, line_vec)
    pt_norm = pt - line_pt - pt_proj
    pt_sym = pt - 2*pt_norm
    return pt_sym

def find_vect_normal(X,Y,Z):
    vect_1 = np.array([X[1,0]- X[1,2],Y[1,0]-Y[1,2],Z[1,0]-Z[1,2]])
    vect_2 = np.array([X[0,1]-X[2,1],Y[0,1]-Y[2,1],Z[0,1]-Z[2,1]])
    return(np.cross(vect_1,vect_2))

def ray_refl(x_ray_inc,y_ray_inc,z_ray_inc,x,y,z,X,Y,Z,i,j,d,ax,option=1):
    mean = []
    if option == 1:
        ask = 'y'
    else :
        ask = 'n'
    vect_normal = find_vect_normal(X,Y,Z)
    pt = np.array([x_ray_inc,y_ray_inc,z_ray_inc])
    line_pt = np.array([x[i,j],y[i,j],z[i,j]])
    x_ray_refl,y_ray_refl,z_ray_refl = [],[],[]
    for k in range(pt.shape[1]):
        coord = find_sym(pt[:,k],line_pt,vect_normal)
        x_ray_refl.append(coord[0])
        y_ray_refl.append(coord[1])
        z_ray_refl.append(coord[2])
    mean.append(np.mean(x_ray_refl))
    mean.append(np.mean(y_ray_refl))
    mean.append(np.mean(z_ray_refl))
    coord = np.array([x_ray_refl,y_ray_refl,z_ray_refl]).T
    coeff = pr.reg_lin_3D(coord)
    t = (d-mean[0])/coeff[0,0]
    yd = coeff[0,1]*t + mean[1]
    zd = coeff[0,2]*t + mean[2] 
    if ask == 'y':
        plt.plot(x_ray_refl,y_ray_refl,z_ray_refl)
        ax.quiver(x[i,j],y[i,j],z[i,j], vect_normal[0], vect_normal[1], vect_normal[2],length=0.35,color='r')    
    return(x_ray_refl,y_ray_refl,z_ray_refl,yd,zd,vect_normal)

def plot_ecran(a,c,modes,temps,theta_0,d,d_inc,x_repos,y_repos,fig,ax):
    ask = 'y'
    H = [[],[]] # Coordonnées sur l'écran
    for t in temps :
        print(t)
        r,theta,x,y,z_membrane = ts.trace_membrane(a,c,modes,t,fig,ax,option=0)
        x_ray_inc,y_ray_inc,z_ray_inc = rayon_incident(theta_0,d_inc,x_repos,y_repos,option=0)
        i,j = intersection(x,y,z_membrane,theta_0,d_inc,x_repos,y_repos,option=0)
        X,Y,Z_plan = tpt.plan_tangent(r,theta,x,y,z_membrane,i,j,fig,ax,option=0)
        x_ray_refl,y_ray_refl,z_ray_refl,y_intersec,z_intersec = ray_refl(x_ray_inc,y_ray_inc,z_ray_inc,x,y,z_membrane,X,Y,Z_plan,i,j,d,ax,option=0)
        H[0].append(y_intersec)
        H[1].append(z_intersec)
    if ask == 'y':
        plt.figure()
        plt.plot(H[0],H[1],'r')
        plt.grid()
        plt.show()
    return(H)


    
    
