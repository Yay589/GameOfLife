from random import *
from parametre import *
from random import shuffle
from math import trunc
from nourriture import *
from case import Case
from bob import Bob
from affichage import *
import collections

if __name__ == '__main__':
    
    bob1 = Bob(bobSpeed = 1, bobPerception = 1, coord = (0,0))
    allBobs.append(bob1)
    
    ajouterNourritureCase((4,4))
    ajouterNourritureCase((0,3))
    
    for i in range(15):
        print(i)
        afficheGrilleSimple()
        #bob1.speak()
        if(not bob1.reproduction()):
            if(not bob1.manger()):
                if(bob1.setNourritureEnVue()): #on teste si le bob voit des nourritures
                    bob1.setNourriturePreferee()
                    print(bob1.coordNourriturePref)
                    bob1.beeline(bob1.coordNourriturePref)
                else:
                    bob1.bouger()
    for b in allBobs:
        b.speakPerception()
        
    
    # afficheGrilleSimple()
    
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