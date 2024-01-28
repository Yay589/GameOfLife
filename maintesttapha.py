import curses
import pickle
from random import *
from parametre import *
from math import trunc
from nourriture import *
from case import Case
from bob import Bob
from affichage import *
import collections
import time
import random
from itertools import count

#fonction pour avoir des infos globales sur notre grille
def avgSpeed():
    i = 0
    speedSum = 0
    for c in grille:
        for b in grille[c].bobs :
            speedSum += b.speed
            i += 1
    if(i==0):
        print("Tout les bobs sont morts")
        return(-1)
    else:
        return speedSum/i



if __name__ == '__main__':
        for i in range(numberBob):
            allBobs.append(Bob(coord=(randint(0,N-1),randint(0,N-1)),bobPerception=10))
        
        afficheGrilleSimpleCouleur(0,0)
        day = 0
        for j in count():
            #os.system("clear")  
            print("Debut de journée")
            renouvellerNourriture()
            for k in range(T):
                
                print("\033[H\033[J",end="")
                random.shuffle(allBobs) #Pour que ca ne soit pas toujours les memes bobs qui bougent en premier
                time.sleep(0.5)
                for b in allBobs:
                    b.avantUnTour()
                    if(not b.dejaJoue() and not b.seProteger() and not b.reproductionSexuee() and not b.reproduction()):
                        b.partageEnergie()
                        if(not b.manger() and not b.attaque() and (not educationON or not b.eduquer())):
                            b.bobDeplacement()
                print("\033[H\033[J",end="")
                afficheGrilleSimpleCouleurEducation(k, j)
                time.sleep(0.1)
        
        
        
            
          
            





