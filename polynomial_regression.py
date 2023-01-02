#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:01:43 2022

@author: theofauvet
"""

import numpy as np

def reg_lin_3D(data):
    datamean = data.mean(axis=0)
    uu, dd, vv = np.linalg.svd(data - datamean)
    return vv
    

