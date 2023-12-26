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
    
    bob1 = Bob(bobSpeed = 1, bobPerception = 4,bobMemory=2, coord = (2,2))
    allBobs.append(bob1)
    
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
    
    for i in range(10):
        afficheGrilleSimple()
        bob1.bobDeplacement()
        bob1.speak()
        print(bob1.casesMemorisee)
    
    """
    bob1.bouger()
    afficheGrilleSimple()
    bob1.setNourritureEnVue()
    print(bob1.coordAdjacentes)
    print(bob1.nourritureEnVue)
    """
    
    
    #print(bob1.seul())
    #print(bob1.choisirUnBob())
    
    #bob1.bouger()