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

if __name__ == '__main__':
    for i in range(10):
        allBobs.append(Bob(bobPerception=6, coord=(randint(0,N-1),randint(0,N-1))))
    
    """
    renouvellerNourriture()
    
    for i in range(8):
        print(i) 
        afficheGrilleSimple()
        for b in allBobs:
            print(b.coordClosestPrey)
            if(not b.dejaJoue() and not b.seProteger() and not b.manger()):
                b.bobDeplacement()
    
    
    #test du fonctionnnement global du jeu
    """
    
    for k in range(25):
        for j in range(7):
            renouvellerNourriture()
            for i in range(20):
                for b in allBobs:
                    if(not b.dejaJoue() and not b.seProteger() and not b.reproductionSexuee() and not b.reproduction() and not b.manger()):
                        b.bobDeplacement()
                print("\033[H\033[J",end="")
                afficheGrilleSimpleCouleur()
                time.sleep(0.05)


    
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