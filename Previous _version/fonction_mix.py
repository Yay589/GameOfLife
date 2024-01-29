from random import *
from parametre import *
from math import trunc
from nourriture import Nourriture
from case import Case
from bob import Bob
from affichage import *


def viderNourritureGrille():
    caseSuprCoord = []
    for c in grille:
        grille[c].viderNourriture()
        if(grille[c].estVide()):
            caseSuprCoord.append(c)
    for c2 in caseSuprCoord:
        grille[c2].supprimer()
    
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


def nbBobs():
    i = 0
    for c in grille:
        for b in grille[c].bobs :
            i += 1
    return i
    

def fonction_mix():
    for i in range(N-1):
        allBobs.append(Bob(coord = (randint(0,N-1),randint(0,N-1))))
    allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(2*N)]
    
    bob_ex = Bob( bobEnergy=bobMaxE, coord = (0,0))
    allBobs.append(bob_ex)

    i=0

    for i in range(40):
        viderNourritureGrille()
        allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(N*2)]
        for j in range(T):
            for b in allBobs:
                if(not b.reproduction()):
                    if(not b.manger()):
                        b.bouger()