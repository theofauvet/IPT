#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 00:11:42 2022

@author: theofauvet
"""

from scipy.special import jv, jn_zeros

def root(L):
    return(L[0])

def order_modes(M,N):
    list_root = []
    for m in range(0,M):
        root = jn_zeros(m,N)
        for k in range(0,len(root)):
            list_root.append([root[k],(m,k+1)])
    return(list_root)

def root_sort(M,N):
    A = order_modes(M,N)
    return(sorted(A, key=root))
