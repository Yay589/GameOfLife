from random import *
from parametre import *
from random import shuffle
from math import trunc
from nourriture import *
from case import Case
from bob import Bob
from affichage import *
import collections

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


def nbBobs(): #c'est la même taille que len(allBobs) normalement
    i = 0
    for c in grille:
        for b in grille[c].bobs :
            i += 1
    return i

def allBobsSpeak():
    for b in allBobs:
         b.speakPerception()

if __name__ == '__main__':
    
    for i in range(numberBob):
        allBobs.append(Bob())
        
    #bob1 = Bob(bobEnergy=200,bobSpeed = 1, bobPerception = 4,bobMemory=2, coord = (0,0))
    #bob2 = Bob(bobEnergy=200,bobSpeed = 1.5, bobPerception = 2,bobMemory=5, coord = (2,2))
    #allBobs.append(bob1)
    #allBobs.append(bob2)
    
    for k in range(25):
        #print("debut semaine")
        for j in range(7):
            renouvellerNourriture()
            for i in range(T):
                for b in allBobs:
                    if(not b.dejaJoue() and not b.reproductionSexuee() and not b.reproduction() and not b.manger()):
                        b.bobDeplacement()
        #print("fin semaine")
        #afficheGrilleSimple()
        print("Semaine ",k)
        print("nombre de bob en vie : ", nbBobs())
        if(nbBobs() == 0):
            print("Tout les bobs sont morts")
        else:
            print("Vitesse moyenne des bobs : ",avgSpeed())
            print("Perception moyenne : ",avgPerception())
            print("Memoire moyenne : ",avgMemory())
        #allBobsSpeak()

    
    # ajouterNourritureCase((4,4))
    # ajouterNourritureCase((4,3))
    # ajouterNourritureCase((3,4))
    # ajouterNourritureCase((1,0))
    # ajouterNourritureCase((0,0))
    
    """
    
    afficheGrilleSimple()
    for i in range(20):
        if(not bob1.reproduction()):
            if(not bob1.manger()):
                bob1.bobDeplacement()
        print("cases memorisées : ",bob1.casesMemorisee)
        print("nourriture memorisées : ",bob1.nourritureMemorisee)
        afficheGrilleSimple()
    
    allBobsSpeak()
    
         
    afficheGrilleSimple()
    
    """
    
    #print(bob1.seul())
    #print(bob1.choisirUnBob())
    
    #bob1.bouger()