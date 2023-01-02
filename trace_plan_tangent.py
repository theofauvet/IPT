#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 18:15:52 2022

@author: theofauvet
"""

import matplotlib.pyplot as plt
import numpy as np

import scipy.linalg

import itertools

def plan_tangent(r,theta,x,y,z,i,j,fig,ax,option=1):
    if option == 1:
        ask = 'y'
    else:
        ask = 'n' 
    data_x = list(itertools.chain(*x[i:i+2,j:j+6].tolist()))
    data_y = list(itertools.chain(*y[i:i+2,j:j+6].tolist()))
    data_z = list(itertools.chain(*z[i:i+2,j:j+6].tolist()))
    data = np.array([data_x,data_y,data_z])
    data = data.T    
    X,Y = np.meshgrid(np.arange(x[i,j]-0.5, x[i,j]+1, 0.5), np.arange(y[i,j]-0.5, y[i,j]+1, 0.5))   
    A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients        
    Z = C[0]*X + C[1]*Y + C[2]
           
    if ask == 'y':       
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.8)
        #plt.plot(data[:,0],data[:,1],data[:,2],'go')
        # plt.plot(X[1,0],Y[1,0],Z[1,0],'ro')
        # plt.plot(X[1,2],Y[1,2],Z[1,2],'ro')
        # plt.plot(X[0,1],Y[0,1],Z[0,1],'go')
        # plt.plot(X[2,1],Y[2,1],Z[2,1],'go')
        # plt.plot(x[i,j],y[i,j],z[i,j],'mo')
        plt.xlabel('X')
        plt.ylabel('Y')
        ax.set_zlabel('Z')
        ax.axis('equal')
        ax.axis('tight')
        plt.show()
    return(X,Y,Z)






