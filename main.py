from random import *
from parametre import *
from math import trunc
from nourriture import *
from case import Case
from bob import Bob
from affichage import *

#fonction pour avoir des infos globales sur notre grille
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
        return speedSum/i

def nbBobs():
    i = 0
    for c in grille:
        for b in grille[c].bobs :
            i += 1
    return i


if __name__ == '__main__':
        for i in range(N - 1):
            allBobs.append(Bob(coord=(randint(0, N - 1), randint(0, N - 1))))
        renouvellerNourriture()

        afficheGrille()
        print(grille)