from parametre import *

def avgSpeed():
    i = 0
    speedSum = 0
    for c in grille:
        for b in grille[c].bobs :
            speedSum += b.speed
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(speedSum/i)
    
def avgPerception():
    i = 0
    perceptionSum = 0
    for c in grille:
        for b in grille[c].bobs :
            perceptionSum += b.perception
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(perceptionSum/i)
    
def avgMemory():
    i = 0
    memSum = 0
    for c in grille:
        for b in grille[c].bobs :
            memSum += b.memory
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(memSum/i)

def avgMass():
    i = 0
    massSum = 0
    for c in grille:
        for b in grille[c].bobs :
            massSum += b.mass
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(massSum/i)
    
def avgEnergy():
    i = 0
    energySum = 0
    for c in grille:
        for b in grille[c].bobs :
            energySum += b.energy
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(energySum/i)


def nbBobs(): #c'est la même taille que len(allBobs) normalement
    i = 0
    for c in grille:
        for b in grille[c].bobs :
            i += 1
    return i
    
def maxSpeed():
    i = 0
    maxSpeed = 0
    for c in grille:
        for b in grille[c].bobs :
            if(b.speed > maxSpeed):
                maxSpeed = b.speed
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(maxSpeed)
    
def minSpeed():
    i = 0
    minSpeed = avgSpeed()
    for c in grille:
        for b in grille[c].bobs :
            if(b.speed < minSpeed):
                minSpeed = b.speed
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(minSpeed)

def maxMass():
    i = 0
    maxMass = 0
    for c in grille:
        for b in grille[c].bobs :
            if(b.mass > maxMass):
                maxMass = b.mass
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(maxMass)
    
def minMass():
    i = 0
    minMass = avgMass()
    for c in grille:
        for b in grille[c].bobs :
            if(b.mass < minMass):
                minMass = b.mass
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(minMass)
    
def maxPerception():
    i = 0
    maxPerception = 0
    for c in grille:
        for b in grille[c].bobs :
            if(b.perception > maxPerception):
                maxPerception = b.perception
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(maxPerception)
    
def minPerception():
    i = 0
    minPerception = avgPerception()
    for c in grille:
        for b in grille[c].bobs :
            if(b.perception < minPerception):
                minPerception = b.perception
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(minPerception)
    
def maxMemory():
    i = 0
    maxMemory = 0
    for c in grille:
        for b in grille[c].bobs :
            if(b.memory > maxMemory):
                maxMemory = b.memory
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(maxMemory)
    
def minMemory():
    i = 0
    minMemory = avgMemory()
    for c in grille:
        for b in grille[c].bobs :
            if(b.memory < minMemory):
                minMemory = b.memory
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(minMemory)
    
def maxEnergy():
    i = 0
    maxEnergy = 0
    for c in grille:
        for b in grille[c].bobs :
            if(b.energy > maxEnergy):
                maxEnergy = b.energy
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(maxEnergy)
    
def minEnergy():
    i = 0
    minEnergy = avgEnergy()
    for c in grille:
        for b in grille[c].bobs :
            if(b.energy < minEnergy):
                minEnergy = b.energy
            i += 1
    if(i==0):
        print("Tout les bobs sont mort")
        return(-1)
    else:
        return(minEnergy)
    
def minChosenCaracteristic():
    if(chosenCarateristic == VITESSE):
        return minSpeed()
    elif(chosenCarateristic == MASSE):
        return minMass()
    elif(chosenCarateristic == PERCEPTION):
        return minPerception()
    elif(chosenCarateristic == MEMOIRE):
        return minMemory()
    elif(chosenCarateristic == ENERGIE):
        return 0
    
def maxChosenCaracteristic():
    if(chosenCarateristic == VITESSE):
        return maxSpeed()
    elif(chosenCarateristic == MASSE):
        return maxMass()
    elif(chosenCarateristic == PERCEPTION):
        return maxPerception()
    elif(chosenCarateristic == MEMOIRE):
        return maxMemory()
    elif(chosenCarateristic == ENERGIE):
        return bobMaxE
    
def avgChosenCaracteristic():
    if(chosenCarateristic == VITESSE):
        return avgSpeed()
    elif(chosenCarateristic == MASSE):
        return avgMass()
    elif(chosenCarateristic == PERCEPTION):
        return avgPerception()
    elif(chosenCarateristic == MEMOIRE):
        return avgMemory()
    elif(chosenCarateristic == ENERGIE):
        return bobMaxE/2
    
