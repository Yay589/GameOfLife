"""
Ce fichier contient les fonctions qui permettent de faire un affichage terminal pour notre jeu

3 affichages differents disponible

"""

__date__ = "2023-10-12"


from parametre import *
from nourriture import *
from case import Case
from bob import Bob
from math import *
from statistiques import *


def afficheGrilleSimpleCouleur(tick, day):
    vitesseMoy = avgSpeed()
    vitesseMax = maxSpeed()
    vitesseMin = minSpeed()
    masseMoy = avgMass()
    masseMax = maxMass()
    masseMin = minMass()
    perceptionMoy = avgPerception()
    perceptionMax = maxPerception()
    perceptionMin = minPerception()
    memoireMoy = avgMemory()
    memoireMax = maxMemory()
    memoireMin = minMemory()
    energieMoy = avgEnergy()
    energieMax = maxEnergy()
    energieMin = minEnergy()
    
    
    parametreAffichageMoy = avgChosenCaracteristic()
    parametreAffichageMin = minChosenCaracteristic()
    parametreAffichageMax = maxChosenCaracteristic()
    
    print("Jour : ",day,"Tic : ",tick)
    print("Nombre de bob vivant : ",len(allBobs),"  Nombre de bobs morts : ",len(deadBobs))
    print("Energie moyenne : ",trunc(energieMoy*1000)/1000,"Energie minimale : ", trunc(energieMin*1000)/1000, "Energie maximum : ",trunc(energieMax*1000)/1000)
    if(speedON):
        print("Vitesse moyenne : ",trunc(vitesseMoy*1000)/1000,"Vitesse minimale : ", trunc(vitesseMin*1000)/1000, "Vitesse maximum : ",trunc(vitesseMax*1000)/1000)
    if(massON):
        print("Masse moyenne : ",trunc(masseMoy*1000)/1000,"Masse minimale : ", trunc(masseMin*1000)/1000, "Masse maximum : ",trunc(masseMax*1000)/1000)
    if(perceptionON):
        print("Perception moyenne : ",trunc(perceptionMoy*1000)/1000,"Perception minimale : ", trunc(perceptionMin*1000)/1000, "Perception maximum : ",trunc(perceptionMax*1000)/1000)
    if(memoryON):
        print("Mémoire moyenne : ",trunc(memoireMoy*1000)/1000,"Mémoire minimale : ", trunc(memoireMin*1000)/1000, "Mémoire maximum : ",trunc(memoireMax*1000)/1000)
    print("Bob violet : caractéristique choisie < ",(parametreAffichageMin) + 1/4*(parametreAffichageMax-parametreAffichageMin), "bob bleu : caractéristique < ", parametreAffichageMin + 1/2*(parametreAffichageMax-parametreAffichageMin))
    print("Bob vert : caractéristique < ",(parametreAffichageMin) + 3/4*(parametreAffichageMax-parametreAffichageMin), "bob jaune : caractéristique < ",parametreAffichageMax)
    if(deseaseON):
        print("Bob blanc : malade")

    for a in range(M // 2 * 3):
        print(" _", end="")
    print("")
    for i in range(N):
        print("|", end="")
        for j in range(M):
            if ((i, j) in grille):
                if (grille[(i, j)].bobs != []):
                    if(chosenCarateristic == VITESSE):
                        caracteritique = grille[(i, j)].bobs[0].speed
                    elif(chosenCarateristic == MASSE):
                        caracteritique = grille[(i, j)].bobs[0].mass
                    elif(chosenCarateristic == PERCEPTION):
                        caracteritique = grille[(i, j)].bobs[0].perception
                    elif(chosenCarateristic == MEMOIRE):
                        caracteritique = grille[(i, j)].bobs[0].memory
                    elif(chosenCarateristic == ENERGIE):
                        caracteritique = grille[(i, j)].bobs[0].energy
                    
                    if (deseaseON and grille[(i,j)].bobs[0].sick):
                        print("\033[0;37m ○ \033[0;30m", end="") # blanc
                    elif (caracteritique < ((parametreAffichageMin) + 1/4*(parametreAffichageMax-parametreAffichageMin))):
                        print("\033[0;35m ○ \033[0;30m", end="") #rose 35
                    elif ((caracteritique < (parametreAffichageMin + 1/2*(parametreAffichageMax-parametreAffichageMin))) and (caracteritique >= (parametreAffichageMin + 1/4*(parametreAffichageMax-parametreAffichageMin)))):
                        print("\033[0;34m ○ \033[0;30m", end="") #bleu 34
                    elif ((caracteritique < (parametreAffichageMin + 3/4*(parametreAffichageMax-parametreAffichageMin))) and (caracteritique>= (parametreAffichageMin + 1/2*(parametreAffichageMax-parametreAffichageMin)))):
                        print("\033[0;32m ○ \033[0;30m", end="")#vert 32
                    elif (caracteritique >= (parametreAffichageMin + 3/4*(parametreAffichageMax-parametreAffichageMin))):
                        print("\033[0;33m ○ \033[0;30m", end="")#jaune 33
                else:
                    print("\033[0;31m  \033[0;30m", end="")
            else:
                print("   ", end="")
        print("|", end="")
        print("")
    for a in range(M // 2 * 3):
        print(" _", end="")
    print("\n")

# version d'affichage avec des contours, pour une petite grille
def afficheGrille():
    for a in range(int(N * 4.5)):
        print(" _", end="")
    print("")
    for i in range(N):
        print("|", end="")
        for j in range(N):
            if ((i, j) in grille):
                if (grille[(i, j)].bobs != []):
                    if (grille[(i, j)].qtite_nourriture != 0):
                        print(" ^^ ", grille[(i, j)].qtite_nourriture, "", end="")
                    elif (len(grille[(i, j)].bobs) == 1):
                        print("  (^-^)  ", end="")
                    elif (len(grille[(i, j)].bobs) == 2):
                        print("(^^) (^^)", end="")
                    elif (len(grille[(i, j)].bobs) == 2):
                        print(" 3+ bobs ", end="")
                else:
                    print("  ", grille[(i, j)].qtite_nourriture, "  ", end="")
            else:
                print("         ", end="")
        print("|", end="")
        print("")
    for a in range(int(N * 4.5)):
        print(" _", end="")
    print("")

# version d'affichage "emoji" fonctionne pour des grilles un peu plus grande (environ 35*35)
def afficheGrilleSimple():
    for a in range(N // 2 * 5):
        print(" _", end="")
    print("")
    for i in range(N):
        print("|", end="")
        for j in range(N):
            if ((i, j) in grille):
                if (grille[(i, j)].bobs != []):
                    if (grille[(i, j)].qtite_nourriture != 0 and len(grille[(i, j)].bobs) == 1):
                        print(" ○♥  ", end="")
                    elif (grille[(i, j)].qtite_nourriture != 0 and len(grille[(i, j)].bobs) == 2):
                        print(" ○♥○ ", end="")
                    elif (grille[(i, j)].qtite_nourriture != 0 and len(grille[(i, j)].bobs) > 2):
                        print(" b&f ", end="")
                    elif (len(grille[(i, j)].bobs) == 1):
                        print("  ○  ", end="")
                    elif (len(grille[(i, j)].bobs) == 2):
                        print(" ○○  ", end="")
                    elif (len(grille[(i, j)].bobs) == 3):
                        print(" ○○○ ", end="")
                    elif (len(grille[(i, j)].bobs) > 3):
                        print(" bbb ", end="")
                else:
                    print("  ♥  ", end="")
            else:
                print("     ", end="")
        print("|", end="")
        print("")
    for a in range(N // 2 * 5):
        print(" _", end="")
    print("\n")

def afficheGrilleSimple():
    for a in range(N // 2 * 3):
        print(" _", end="")
    print("")
    for i in range(N):
        print("|", end="")
        for j in range(N):
            if ((i, j) in grille):
                if (grille[(i, j)].bobs != []):
                    if (grille[(i, j)].qtite_nourriture != 0 and len(grille[(i, j)].bobs) == 1):
                        print("○♥ ", end="")
                    elif (grille[(i, j)].qtite_nourriture != 0 and len(grille[(i, j)].bobs) == 2):
                        print("○♥○", end="")
                    elif (grille[(i, j)].qtite_nourriture != 0 and len(grille[(i, j)].bobs) > 2):
                        print("b&f", end="")
                    elif (len(grille[(i, j)].bobs) == 1):
                        print(" ○ ", end="")
                    elif (len(grille[(i, j)].bobs) == 2):
                        print("○○ ", end="")
                    elif (len(grille[(i, j)].bobs) == 3):
                        print("○○○", end="")
                    elif (len(grille[(i, j)].bobs) > 3):
                        print("bbb", end="")
                else:
                    print(" ♥ ", end="")
            else:
                print("   ", end="")
        print("|", end="")
        print("")
    for a in range(N // 2 * 3):
        print(" _", end="")
    print("\n")

# affichage avec des cases separées (petite grille)
def afficheGrilleCrochet():
    for i in range(N):
        for j in range(N):
            if ((i, j) in grille):
                if (grille[(i, j)].bobs != []):
                    if (grille[(i, j)].qtite_nourriture != 0):
                        print("[ ^^ ", grille[(i, j)].qtite_nourriture, "]", end="")
                    elif (len(grille[(i, j)].bobs) == 1):
                        print("[  (^-^)  ]", end="")
                    elif (len(grille[(i, j)].bobs) == 2):
                        print("[(^^) (^^)]", end="")
                    elif (len(grille[(i, j)].bobs) >= 3):
                        print("[ 3+ bobs ]", end="")
                else:
                    print("[  ", grille[(i, j)].qtite_nourriture, "  ]", end="")
            else:
                print("[         ]", end="")
        print("")
