import pickle
from parametre import *
from math import trunc
from nourriture import *
from case import Case
from bob import Bob
from affichage import *
import collections
import time
import random


# fonction pour avoir des infos globales sur notre grille
def avgSpeed():
    i = 0
    speedSum = 0
    for c in grille:
        for b in grille[c].bobs:
            speedSum += b.speed
            i += 1
    if (i == 0):
        print("Tous les bobs sont morts")
        return (-1)
    else:
        return speedSum / i


if __name__ == '__main__':
    # for x in range(T):
    for i in range(100):
        allBobs.append(Bob(coord=(randint(0, N - 1), randint(0, N - 1)), bobPerception=10))
        # allBobs[i].speak()

    j = 0
    for j in range(7):
        # os.system("clear")
        print("Debut de journée")
        if (len(allBobs) == 0):
            break
        j+=1
        renouvellerNourriture()
        for k in range(T):
            print("\033[H\033[J", end="")
            afficheGrilleSimpleCouleur()
            time.sleep(0.5)
            random.shuffle(allBobs)
            for b in allBobs:
                if not b.dejaJoue() and not b.seProteger() and not b.attack() and not b.manger() and not b.reproduction():
                    b.bobDeplacement()
                    b.speak()


        afficheGrilleSimpleCouleur()


# print("fin des 10 jours : ")
#print("vitesse moyenne des bobs : ",avgSpeed())
print("nombre de bob en vie : ", len(allBobs))