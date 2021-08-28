# IMPORTS
import numpy as np
import math

# MAIN

def computeW(N):
    I = 360/N # Interior Angle
    
    distList =  []
    
    for j in range(1,N): 
        dist = np.sqrt(2 - (2*np.cos(I * j * (np.pi/180) ))) # cosine rule
        distList.append(dist)
        
    for i in range(len(distList)): # converting dist to W values
        distList[i] = 1/distList[i]
        
    W = sum(distList) * N / 2

    print("N = " + str(N) + ": W = " + str(W))

for i in range(1,60):
    computeW(i)
