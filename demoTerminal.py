from random import *
from parametre import *
from random import shuffle
from math import trunc
from nourriture import *
from case import Case
from bob import Bob
from affichage import *
import collections
import time

def allBobsSpeakM():
    for b in allBobs:
        if(not b.dead):
            b.speakMass()

def allBobsSpeakS():
    for b in allBobs:
        b.speakSpeed()

def allBobsPrevious():
    for b in allBobs:
        b.speakPreviousAction()

def allBobsPreviousNotRandomMove():
    for b in allBobs:
        if(b.previousAction != DEPLACEMENT_ALEATOIRE):
            b.speakPreviousAction()
        

if __name__ == '__main__':
    allBobs = []
    allBobs.append(Bob(bobPerception=0,bobMemory=2, bobEnergy=199,bobSpeed=2,bobMass=2, coord=(2,3)))
    allBobs.append(Bob(bobPerception=4,bobMemory=2,bobEnergy=199 , bobSpeed=1,bobMass=1, coord=(1,3)))
    
    ajouterNourritureCaseSpecifique((1,1))

    print("\033[H\033[J",end="")
    print("On met deux bobs à distance égale d'une nourriture avec un perception très grande \n pour qu'ils aillent chercher la nourriture")
    afficheCouleur(0,0)
    sleep(0.5)
    #print("\033[H\033[J",end="")

    

    day = 0
    for k in range(10):
        day += 1
        tick = 0            
        for i in range(5):
            tick += 1
            for b in allBobs:
                b.avantUnTour()
                
                if(not b.dejaJoue() and not b.seProteger() and not b.reproductionSexuee() and not b.reproduction()):
                    b.partageEnergie()
                    if(not b.manger() and not b.attaque() and (not educationON or not b.eduquer())):
                        b.bobDeplacement()
            afficheCouleur(tick, day)
            allBobsSpeakM()
            sleep(0.5)
            print("\033[H\033[J",end="")

            