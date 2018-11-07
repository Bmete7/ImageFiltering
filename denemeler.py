# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:01:54 2018

@author: BurakBey
""" 

import numpy as np
import math

def cubicInterpolation(pix,x):
    p1 = pix[0]
    p2 = pix[1] 
    p3 = pix[2] 
    p4 = pix[3]
    a =  p2
    b = (-1/2) * p1 + p3/2
    c = p1 - (5/2) * p2 + 2*p3 - p4/2
    d = -1 * p1/2 + (3/2) * p2 - (3/2) * p3 + p4/2
    
    return (a) + (b * math.pow(x,1))+(c * math.pow(x,2))+((d * math.pow(x,3)))



def calculateInterpolation(x,y):
    srcx = int(x / coef)
    xfrc = x/coef - srcx
    
    srcy = int(y/coef)
    yfrc = y/coef - srcy
    
    pixels = np.zeros((4,4) , dtype='int32')

    for i in range(-1,3):
        for j in range(-1,3):
            if(x+i >= 0 and srcx+i < h and y+j >= 0 and srcy+j < w ):
                pixels[i+1,j+1] = im[srcx+i,srcy+j]
    if(x==0 and y == 0):
        print(pixels)
    cols = np.zeros((4,1) , dtype='int32')
    for i in range(0,4):
        cols[i,0] = cubicInterpolation(pixels[i,:], xfrc)
    if(x==0 and y == 0):
        print(cols)
    val = cubicInterpolation(cols[:,0] , yfrc)
    if(x==0 and y == 0):
        print(val)
    if(val<0): 
        val = 0
    if(val >= 255):
        val = 255
    return int(val)

im = np.random.rand(70,90)
im *= 255
h,w= im.shape
coef = 2
x= h*coef
y=w*coef
im = im.astype(int)
out = np.zeros((x,y), dtype='int32')

for i in range(0,x):
    for j in range(0,y):
        out[i,j] = calculateInterpolation(i,j)
        
        
    

    
    