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
        b.speakMass()

def allBobsPrevious():
    for b in allBobs:
        b.speakPreviousAction()

def allBobsPreviousNotRandomMove():
    for b in allBobs:
        if(b.previousAction != DEPLACEMENT_ALEATOIRE):
            b.speakPreviousAction()
        

if __name__ == '__main__':
    #for i in range(numberBob):
    #    allBobs.append(Bob(bobPerception=6, coord=(randint(0,N-1),randint(0,M-1))))

    allBobs = []
    allBobs.append(Bob(bobPerception=2,bobMemory=0,bobEducation = True, bobEnergy=100,bobSpeed=1,bobMass=1, coord=(2,2)))
    #allBobs.append(Bob(bobEducation = False, bobEnergy=199 , bobSpeed=1,bobMass=1, coord=(2,0)))
    allBobs.append(Bob(bobPerception=2,bobEducation = False, bobEnergy=80, bobSpeed=1,bobMass=1, coord=(0,0)))

    ajouterNourritureCaseSpecifique((2,1))


    print("\033[H\033[J",end="")
    afficheGrilleSimpleCouleurEducation(0, 0)
    print("Etat actuel des bobs : ")
    for b in allBobs:
        b.speakEducationKindness()
    sleep(0.80)
    
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
            print("\033[H\033[J",end="")
            afficheGrilleSimpleCouleurEducation(tick, day)
            print("Etat actuel des bobs : ")
            #for b in allBobs:
            #    b.speakEducationKindness()
            sleep(0.60)
     
    """        
    day = 0
    for k in range(10):
        day += 1
        tick = 0
        renouvellerNourriture()
            
        for i in range(5):
            tick += 1
            for b in allBobs:
                b.avantUnTour()
                if(not b.dejaJoue() and not b.seProteger() and not b.reproductionSexuee() and not b.reproduction()):
                    b.partageEnergie()
                    if(not b.manger() and not b.attaque() and (not educationON or not b.eduquer())):
                        b.bobDeplacement()
            print("\033[H\033[J",end="")
            afficheGrilleSimpleCouleurEducation(tick, day)
        """
            
            