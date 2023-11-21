from random import *
from parametre import *
from math import trunc
from nourriture import Nourriture
from case import Case
from bob import Bob
from affichage import *

#fonction pour avoir des infos globales sur notre grille

def viderNourritureGrille():
    caseSuprCoord = []
    for c in grille:
        grille[c].viderNourriture()
        if(grille[c].estVide()):
            caseSuprCoord.append(c)
    for c2 in caseSuprCoord:
        grille[c2].supprimer()
    
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


def nbBobs():
    i = 0
    for c in grille:
        for b in grille[c].bobs :
            i += 1
    return i
    

if __name__ == '__main__':
    #main de demonstration des fonctions
    
    #exemple affichages
    for i in range(N-1):
        allBobs.append(Bob(coord = (randint(0,N-1),randint(0,N-1))))
    allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(2*N)]
    
    bob_ex = Bob( bobEnergy=bobMaxE, coord = (0,0))
    allBobs.append(bob_ex)
    
    print("Trois models d'affichage différents : ")
    print("Avec des cases distinctes")
    afficheGrilleCrochet()
    print("Sans les cases")
    afficheGrille()
    print("Version plus condensée pour afficher une grille plus grande")
    afficheGrilleSimple()

    #fonctions de bases 
    print("Exemple d'utilisation très simple des fonction de bases :")
    print("Notre monde : ")
    afficheGrilleSimple()
    print("Chaque bob à le droit à une action : ")
    i=0
    for b in allBobs:
        i += 1
        print("\nBob n°",i)
        b.speak()
        if(b.birthDay == 1):
            b.speakSpeed()
            b.birthDay = 0
            print("Je viens de naître, j'attends le prochain tic pour faire une action")
        elif(not b.reproduction()):
            if(not b.manger()):
                print("je bouge")
                b.bouger()
                b.speak()
            else:
                print("je mange")
                b.speak()
                        
        else:
            print("je fais un bebe")
            b.speakSpeed()
    print("\nNotre monde après que chaque bob ai fait son action : ")
    afficheGrilleSimple()
    
    
    
    
    #exemple sur 5 jours
    print("Exemple de fonctionnement du jeu sur 5 jours avec une toute petite grille et peu de bobs")
    for i in range(5):
        print("Jour : ",i)
        viderNourritureGrille()
        allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(N*2)]
        print("debut de la journée :")
        afficheGrilleSimple()
        for j in range(T):
            for b in allBobs:
                if(not b.reproduction()):
                    if(not b.manger()):
                        b.bouger()
        print("fin de la journée : ")
        afficheGrilleSimple()
    
    print("fin des 5 jours : ")
    print("vitesse moyenne des bobs : ",avgSpeed())
    print("nombre de bob en vie : ", nbBobs())
    
    
    print("\nExemple sur 40 jours avec la même grille ")
    for i in range(40):
        viderNourritureGrille()
        allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(N*2)]
        for j in range(T):
            for b in allBobs:
                if(not b.reproduction()):
                    if(not b.manger()):
                        b.bouger()
    
    print("fin des 40 jours : ")
    print("vitesse moyenne des bobs : ",avgSpeed())
    print("nombre de bob en vie : ", nbBobs(),"\n")
    
    
    #sur 40 jours avec les stats de base du prof (tt les bobs meurent)
    #Paramètres simulation :
    N = 100 #Length or width of the map (grid of N*N)
    NumberB = 100 #Number of Bobs at the begining
    
    T = 100 #Number of ticks in a day
    
    print("\nExemple sur 10 jours avec les stats de l'énoncé :")
    
    allBobs = []
    for i in range(numberBob):
        allBobs.append(Bob(coord = (randint(0,N-1),randint(0,N-1))))
        
    jour = 0
    for i in range(5):
        if(nbBobs()==0):
            break
        jour += 1
        viderNourritureGrille()
        allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(numberFood)]
        for j in range(T):
            for b in allBobs:
                if(not b.reproduction()):
                    if(not b.manger()):
                        b.bouger()
        print("\nRésultats au bout de ",jour,"jour")
        print("vitesse moyenne des bobs : ",avgSpeed())
        print("nombre de bob en vie : ", nbBobs())
    
    print("\nfin des 10 jours : ")
    print("nombre de bob en vie : ", nbBobs())
    if(nbBobs() == 0):
        print("Tout les bobs sont morts à partir du jour ",jour)
    else:
        print("Vitesse moyenne des bobs : ",avgSpeed())


