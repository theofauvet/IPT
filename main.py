#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:00:34 2022

@author: theofauvet
"""

############################# RESET LES VARIABLES #############################
from IPython import get_ipython
def __reset__(): get_ipython().magic('reset -sf')

__reset__()
###############################################################################

########################## IMPORTATION DES PACKAGES ###########################
import numpy as np
import matplotlib.pyplot as plt

from scipy import signal

from mpl_toolkits.mplot3d import Axes3D 

import matplotlib.animation as animation

import trace_surface as ts
import trace_plan_tangent as tpt
import trace_rayon as tr
import polynomial_regression as pr
import root_sort as rs

###############################################################################

########################## DÉFINITION DES VARIABLES ###########################

a = 1 # Rayon de la membrane - Normalisé
n_o_m = 10 # Nombre de modes que l'on va superposer (*10 car on considère les 10 premiers zéros des 10 premières courbes de Bessel)
modes = [rs.root_sort(n_o_m,n_o_m)[k][1] for k in range(len(rs.root_sort(n_o_m,n_o_m)))] # Indice (n,m) des modes de membrane choisis
c = 1 # Vitesse des ondes - Normalisée
x_repos,y_repos = 0.2,0.1 # Point d'impact du rayon incident sur la membrane à l'instant t = 0
theta_0 = np.pi/4 # Angle que fait le rayon incidient avec la normale à la membrane au point d'impact (voir ci-dessus)
d = 2.5 # Distance entre le point d'impact du rayon incident sur la membrane et l'écran
d_inc = 1 # NE PAS MODIFIER - Paramètre arbitraire pour le tracé des rayons 
w = 3.5 # Pulsation de vibraton du haut-parleur (pulsation de forçage)

###############################################################################

######################### CHOIX DU TRACÉ À RÉALISER ###########################

# case = 0 : Tracé de l'animation membrane + laser sur l'écran
# case = 1 : Tracé du résultat final : figure obtenue sur l'écran
case = 1

                   # PLUS RIEN À MODIFIER À PARTIR D'ICI
###############################################################################

################################ ANIMATION ####################################

if case == 0:

    fig = plt.figure()
    ax1 = fig.add_subplot(1,2,1, projection='3d') # Définition des axes 
    ax1.set_xlim3d(-1,1)
    ax1.set_ylim3d(-1,1)
    ax1.set_zlim3d(-1,1)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    ax2 = fig.add_subplot(1,2,2)
    ax2.set_xlim(-10,10)
    ax2.set_ylim(-10,10)
    ax2.set_xlabel('y')
    ax2.set_ylabel('z')
    ax2.grid()

    N = 150 # Meshsize
    fps = 10 # frame per sec
    frn = 50 # frame number of the animation
    temps = np.linspace(0,20,frn) # Liste des temps sur lesquels les simulations vont être réalisées
    z_array = np.zeros((100,100,frn))
    X_array = np.zeros((3,3,frn))
    Y_array = np.zeros((3,3,frn))
    Z_array = np.zeros((3,3,frn))
    x_inc_array = np.zeros((100,frn))
    y_inc_array = np.zeros((100,frn))
    z_inc_array = np.zeros((100,frn))
    x_refl_array = np.zeros((100,frn))
    y_refl_array = np.zeros((100,frn))
    z_refl_array = np.zeros((100,frn))
    vect_normal_array = np.zeros((3,2,frn))
    ecran_array = np.zeros((2,frn))

    for k in range(len(temps)):
        z = np.zeros((100,100))
        for m in modes:
            r,theta,x,y,z_int = ts.trace_membrane(a,c,m,temps[k],w,fig,ax1,option=0)     
            z+=z_int
        z_array[:,:,k] = z 
        x_ray_inc,y_ray_inc,z_ray_inc = tr.rayon_incident(theta_0,d_inc,x_repos,y_repos,option=0)
        x_inc_array[:,k] = x_ray_inc
        y_inc_array[:,k] = y_ray_inc
        z_inc_array[:,k] = z_ray_inc
        i,j = tr.intersection(x,y,z,theta_0,d_inc,x_repos,y_repos,option=0)
        X,Y,Z = tpt.plan_tangent(r,theta,x,y,z,i,j,fig,ax1,option=0) # Tracé du plan tangent
        X_array[:,:,k] = X
        Y_array[:,:,k] = Y
        Z_array[:,:,k] = Z
        x_ray_refl,y_ray_refl,z_ray_refl,y_intersec,z_intersec,vect_normal = tr.ray_refl(x_ray_inc,y_ray_inc,z_ray_inc,x,y,z,X,Y,Z,i,j,d,ax1,option=0)
        x_refl_array[:,k] = x_ray_refl
        y_refl_array[:,k] = y_ray_refl
        z_refl_array[:,k] = z_ray_refl
        vect_normal_array[:,0,k] = vect_normal
        vect_normal_array[:,1,k] = np.array([x[i,j],y[i,j],z[i,j]])
        ecran_array[:,k] = np.array([y_intersec,z_intersec])
        
    def update_plot(frame_number,X_array,Y_array,Z_array,x_inc_array,y_inc_array,z_inc_array,x_refl_array,y_refl_array,z_refl_array,vect_normal_array,z_array,plot):
        plot[0].remove()
        plot[1].remove()
        plot[2][0].remove()
        plot[3][0].remove()
        plot[4].remove()
        plot[5][0].remove()
        plot[0] = ax1.plot_surface(x, y, z_array[:,:,frame_number], alpha = 0.6,color='b')
        plot[1] = ax1.plot_surface(X_array[:,:,frame_number], Y_array[:,:,frame_number], Z_array[:,:,frame_number],alpha=0.5,color='g')
        plot[2] = ax1.plot(x_inc_array[:,frame_number],y_inc_array[:,frame_number],z_inc_array[:,frame_number],'r')
        plot[3] = ax1.plot(x_refl_array[:,frame_number],y_refl_array[:,frame_number],z_refl_array[:,frame_number],'orange')
        plot[4] = ax1.quiver(vect_normal_array[0,1,frame_number],vect_normal_array[1,1,frame_number],vect_normal_array[2,1,frame_number], vect_normal_array[0,0,frame_number], vect_normal_array[1,0,frame_number], vect_normal_array[2,0,frame_number],length=0.35,color='darkcyan')  
        plot[5] = ax1.plot(vect_normal_array[0,1,frame_number],vect_normal_array[1,1,frame_number],vect_normal_array[2,1,frame_number],'yo')
        
        
    def update_plot_bis(frame_number,ecran_array,plot):
        #plot[0][0].remove()
        plot[0] = ax2.plot(ecran_array[0,frame_number],ecran_array[1,frame_number],'go')
        
    plot = [ax1.plot_surface(x, y, z_array[:,:,0], color='0.75', rstride=1, cstride=1),ax1.plot_surface(X_array[:,:,0], Y_array[:,:,0], Z_array[:,:,0]),ax1.plot(x_inc_array[:,0],y_inc_array[:,0],z_inc_array[:,0]),ax1.plot(x_refl_array[:,0],y_refl_array[:,0],z_refl_array[:,0]),ax1.quiver(vect_normal_array[0,1,0],vect_normal_array[1,1,0],vect_normal_array[2,1,0], vect_normal_array[0,0,0], vect_normal_array[1,0,0], vect_normal_array[2,0,0],length=0.35,color='r'),ax1.plot(vect_normal_array[0,1,0],vect_normal_array[1,1,0],vect_normal_array[2,1,0],'o')]
    plot_b = [ax2.plot(ecran_array[0,0],ecran_array[1,0],'o')]
    ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(X_array,Y_array,Z_array,x_inc_array,y_inc_array,z_inc_array,x_refl_array,y_refl_array,z_refl_array,vect_normal_array,z_array, plot), interval=1000/fps)
    anib = animation.FuncAnimation(fig, update_plot_bis, frn, fargs=(ecran_array,plot_b), interval=1000/fps)
    
    fn = 'plot_surface_animation_funcanimation'
    ani.save(fn+'.mp4',writer='ffmpeg',fps=fps)

########################### TRACÉ RÉSULTAT ÉCRAN ##############################
    
elif case == 1:
    
    fig,ax = plt.subplots()
    n_o_p = 50
    temps = np.linspace(0,20,n_o_p)
    impact_ecran = np.zeros((2,n_o_p))
    
    for k in range(len(temps)):
        z = np.zeros((100,100))
        for m in modes:
            r,theta,x,y,z_int = ts.trace_membrane(a,c,m,temps[k],w,fig,ax,option=0)     
            z+=z_int
        x_ray_inc,y_ray_inc,z_ray_inc = tr.rayon_incident(theta_0,d_inc,x_repos,y_repos,option=0)
        i,j = tr.intersection(x,y,z,theta_0,d_inc,x_repos,y_repos,option=0)
        X,Y,Z = tpt.plan_tangent(r,theta,x,y,z,i,j,fig,ax,option=0) # Tracé du plan tangent
        x_ray_refl,y_ray_refl,z_ray_refl,y_intersec,z_intersec,vect_normal = tr.ray_refl(x_ray_inc,y_ray_inc,z_ray_inc,x,y,z,X,Y,Z,i,j,d,ax,option=0)
        impact_ecran[:,k] = np.array([y_intersec,z_intersec])
        
    plt.plot(impact_ecran[0,:],impact_ecran[1,:],'-o')
    plt.grid()
    plt.show()

###############################################################################





                                                     











