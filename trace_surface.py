#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 15:47:04 2022

@author: theofauvet
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from scipy.special import jv, jn_zeros

Bessel_roots = [jn_zeros(m, 20) for m in range(20)] # Calcul des 10 premiers zéros de chacune des 10 première fonction de Bessel (première espèce)

def lambda_mn(m, n, radius):
    return Bessel_roots[m][n - 1]/radius

def get_vmin_vmax(m, n):
    vmax = np.max(jv(m, np.linspace(0, Bessel_roots[m][n], 100)))
    return -vmax, vmax

def circular_membrane(r, theta, t, m, n, radius, c, w):
    l = lambda_mn(m, n, radius)
    #T = (np.sin(c * l * t) + np.cos(w*t))/(w**2-(l*c)**2) 
    T = (1/((l*c)**2-w**2))*np.cos(w*t)
    R = jv(m, l * r)
    Theta = np.cos(m * theta)
    return R * T * Theta

def trace_membrane(a,c,modes,t,w,fig,ax,option=1):
    if option == 1:
        ask ='y'
    else:
        ask = 'n'
    r = np.linspace(0, a, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    m, n = modes
    r, theta = np.meshgrid(r, theta)
    x = np.cos(theta) * r
    y = np.sin(theta) * r
    vmin, vmax = get_vmin_vmax(m, n)
    z = 1/3*circular_membrane(r, theta, t, m, n, a, c, w)
    if ask == 'y':
        plt.rcParams["figure.figsize"] = [7.00, 3.50]
        plt.rcParams["figure.autolayout"] = True
        ax.plot_surface(x,y,z,alpha=0.8)
    return(r,theta,x,y,z)




     

        
        
        
        
        