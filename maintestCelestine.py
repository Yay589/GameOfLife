from random import *
from parametre import *
from random import shuffle
from math import trunc
from nourriture import *
from case import Case
from bob import Bob
from affichage import *
import collections


def allBobsSpeak():
    for b in allBobs:
         b.speakPerception()

if __name__ == '__main__':
    
    bob1 = Bob(bobEnergy=200,bobSpeed = 1, bobPerception = 4,bobMemory=2, coord = (0,0))
    bob2 = Bob(bobEnergy=200,bobSpeed = 1.5, bobPerception = 2,bobMemory=5, coord = (2,2))
    allBobs.append(bob1)
    allBobs.append(bob2)
    
    for i in range(20):
        for b in allBobs:
            if(not b.dejaJoue()):
                if (not b.reproductionSexuee()):
                    b.bobDeplacement()
        afficheGrilleSimple()
    
    allBobsSpeak()
    
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