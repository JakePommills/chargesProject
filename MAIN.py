"""
MAIN File - W calculator function, and the algorithm  in this file
"""
#!

# IMPORTS:
import random as rd
import pylab as plt
import numpy as np
import time
import copy

# CLASS:
class charge:
    def __init__(self, q):
    # object constructor
        self.q = q # Electrons should be passed as -1

        # Generate charges in square all within circle.
        self.x = rd.uniform(-0.5,0.5)
        self.y = rd.uniform(-0.5,0.5)
    def cfunc(self):
        pass
    
# FUNCTION:
def genCharges(N):
    # Returns a list of length N filled with charge objects.
    OUT = []
    for i in range(N):
        OUT.append(charge(-1))
    return OUT

def findW(chargeList):
    W = 0
    
    for i in range(len(chargeList)):
        for j in range(len(chargeList)):
            
            if i != j:
                
                distx = chargeList[i].x - chargeList[j].x
                disty = chargeList[i].y - chargeList[j].y
                distance = np.sqrt( distx**2 + disty**2)
                
                Wcontribution = (chargeList[i].q * chargeList[j].q)/distance
                W = W + Wcontribution
    W = W / 2 # Remove double counting
    
    return W

def ruleSet(chargeList, T = 1, saveData=False):
    # Apply outlined ruleset to move charges
    
    delta = 0.01
    Wcurrent = findW(chargeList)
    
    # 1. Choose a charge at random.
    randomCharge = rd.choice(range(len(chargeList)))
    # 2. Choose either the x or y coordinate at random.
    randomXorY = rd.choice(["x","y"])
    
    # 3. Increase or decrease randomly the coordinate by delta
    delta = rd.choice([delta, -delta])
    
    if randomXorY == "x":
        chargeList[randomCharge].x += delta
    else:
        chargeList[randomCharge].y += delta
        
    # CHECK THIS NEW VAL IS ALLOWED IN THE CIRCLE if not, keep trying
    while chargeList[randomCharge].x**2 + chargeList[randomCharge].y**2 > 1:
        if randomXorY == "x":
            chargeList[randomCharge].x -= delta
        else:
            chargeList[randomCharge].y -= delta
            
        randomCharge = rd.choice(range(len(chargeList)))
        randomXorY = rd.choice(["x","y"])
        delta = rd.choice([delta, -delta])
        
        if randomXorY == "x":
            chargeList[randomCharge].x += delta
        else:
            chargeList[randomCharge].y += delta
                
                
    # 4. Compute the change in energy dW that results.
    Wtry = findW(chargeList)
    dW = Wtry - Wcurrent
    # 5. If the energy decreases accept the change in the coordinate
    # Not necessary in code but demonstrates rule 5. from notes
    if dW < 0:
        pass
    
    if dW >= 0:
    # 6. If energy increases then accept, probability exp(−∆W/T)
        if rd.random() > np.exp(-dW/T): # fail condition
            if randomXorY == "x":
                chargeList[randomCharge].x -= delta
            else:
                chargeList[randomCharge].y -= delta        
                
    xvals, yvals = [],[]
    for i in range(len(chargeList)):
        xvals.append(chargeList[i].x)
        yvals.append(chargeList[i].y)
        
    return chargeList, [xvals, yvals], Wcurrent


def iterate(iters, chargeList, saveData=False):
    # This function performs "ruleset" multiple times. The function
    # controls temperature T and the data found.
    
    sameCount = 0
    bestW, [xBest, yBest] = 2**16, [0,0]
    [xOld, yOld] = [0,0]
    
    initaltemp = 10000 # initial temperature value
    temp = initaltemp
    tempFactor = 0.9 # amount T decreases every M iterations
    tempControl = 1 # not to change
    for i in range(iters):
        
        # replace the chargelist with the new chargelist
        chargeList, [xNew, yNew], W = ruleSet(chargeList, T = temp)
        
        if W < bestW:
            bestW = W
            [xBest, yBest] = [xNew, yNew]
        

        if [xOld, yOld] == [xNew, yNew]:
            sameCount += 1
        else:
            sameCount = 0
            
        [xOld, yOld] = [xNew, yNew]
        
        
        if np.floor(i/100) == tempControl: # to get every 100th iteration
            tempControl += 1
            temp = tempFactor * temp
            print(i)
            
        if sameCount == 20*len(chargeList): # 20/50 higher 
            # Conclude likely minimum, so reheat system
            temp = initaltemp
            print("Found Likely minima on iteration: " + str(i)  + " ===> W = " + str(bestW))
            
        
            
    # average inner radius:
    innerradList = []
    for i in range(len(chargeList)):
        if np.sqrt( xBest[i]**2 + yBest[i]**2) < 0.9: # 0.9 excludes circumference
            innerradList.append( np.sqrt(xBest[i]**2 + yBest[i]**2) )

    print("-------------------------")        
    print("Best W: " + str( bestW ))
    print("Inner points: " + str(len(innerradList)) + "| Avg rad: " + str(np.mean(innerradList)))

    # PLOTTING
    figure, axes = plt.subplots()    
    draw_circle = plt.Circle((0, 0), 1, fill=False)
    draw_circle2 = plt.Circle((0, 0), 0.001, fill=False)
    axes.add_artist(draw_circle)
    axes.add_artist(draw_circle2)
    plt.scatter( [i for i in xBest], [i for i in yBest], marker = "+", s=200)
    axes.set_xlim(-1.2, 1.2)
    axes.set_ylim(-1.2,1.2)
    plt.axis('off')

    
    
    
    
    
    
    
    
    
# MAIN
start = time.time() # TIME START

charges = genCharges(12) # Make list of N charges

iterate(1000000, charges) # Plot output after M iterations

end = time.time() # TIME END

timetaken = end - start
print("-------------------------")
print("Time taken: "+str(timetaken))
print("-------------------------")
