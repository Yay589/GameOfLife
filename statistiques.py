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
