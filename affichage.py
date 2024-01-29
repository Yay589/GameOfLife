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
from time import * 


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
    kindnessMoy = avgKindness()
    kindnessMax = maxKindness()
    kindnessMin = minKindness()
    
    parametreAffichageMin = minChosenCaracteristic()
    parametreAffichageMax = maxChosenCaracteristic()
    nbmalade = nbBobs_malade()
    longevityMoy = avgLongevity()
    
    print("\033[H\033[J", end="")

    print("Jour : ",day,"Tic : ",tick)
    print("Nombre de bob vivant : ",len(allBobs),"  Nombre de bobs morts : ",len(deadBobs))
    print("Nombre de Bob malade :", nbmalade, "Age moyen :", longevityMoy, "Nombre de bob éduqués : ",nbBobs_educated())
    print("Energie moyenne : ",trunc(energieMoy*1000)/1000,"Energie minimale : ", trunc(energieMin*1000)/1000, "Energie maximum : ",trunc(energieMax*1000)/1000)

    if(speedON):
        print("Vitesse moyenne : ",trunc(vitesseMoy*1000)/1000,"Vitesse minimale : ", trunc(vitesseMin*1000)/1000, "Vitesse maximum : ",trunc(vitesseMax*1000)/1000)
    if(massON):
        print("Masse moyenne : ",trunc(masseMoy*1000)/1000,"Masse minimale : ", trunc(masseMin*1000)/1000, "Masse maximum : ",trunc(masseMax*1000)/1000)
    if(perceptionON):
        print("Perception moyenne : ",trunc(perceptionMoy*1000)/1000,"Perception minimale : ", trunc(perceptionMin*1000)/1000, "Perception maximum : ",trunc(perceptionMax*1000)/1000)
    if(memoryON):
        print("Mémoire moyenne : ",trunc(memoireMoy*1000)/1000,"Mémoire minimale : ", trunc(memoireMin*1000)/1000, "Mémoire maximum : ",trunc(memoireMax*1000)/1000)
    if(kindnessON):
        print("Gentillesse moyenne : ",trunc(kindnessMoy*1000)/1000,"Gentillesse minimale : ", trunc(kindnessMin*1000)/1000, "Gentillesse maximum : ",trunc(kindnessMax*1000)/1000)
    
    if(chosenCarateristic == VITESSE):
        car = "la vitesse"
    elif(chosenCarateristic == MASSE):
        car= "la masse"
    elif(chosenCarateristic == PERCEPTION):
        car="la perception"
    elif(chosenCarateristic == MEMOIRE):
        car= "la mémoire"
    elif(chosenCarateristic == ENERGIE):
        car="l'énergie"
    
    print("Couleur en fonction de la valeur de",car," : ")
    print("\033[0;35mviolet\033[0;30m < ",trunc((parametreAffichageMin + 1/4*(parametreAffichageMax-parametreAffichageMin))*1000)/1000, "\033[0;34mbleu\033[0;30m < ", trunc((parametreAffichageMin + 1/2*(parametreAffichageMax-parametreAffichageMin))*1000)/1000, "\033[0;32mvert\033[0;30m < ",trunc((parametreAffichageMin + 3/4*(parametreAffichageMax-parametreAffichageMin))*1000)/1000, "\033[0;33mjaune\033[0;30m < ",trunc(parametreAffichageMax*1000)/1000)
    if(deseaseON):
        print("Bob \033[0;37mblanc\033[0;30m : malade")
    

    for a in range(M // 2 * 3):
        print(" _", end="")
    print("")
    for i in range(N):
        print("|", end="")
        for j in range(M):
            if ((i, j) in grille):
                if (grille[(i, j)].bobs != []):
                    b = grille[(i, j)].bobs[0]
                    if(chosenCarateristic == VITESSE):
                        caracteritique = b.speed
                    elif(chosenCarateristic == MASSE):
                        caracteritique = b.mass
                    elif(chosenCarateristic == PERCEPTION):
                        caracteritique = b.perception
                    elif(chosenCarateristic == MEMOIRE):
                        caracteritique = b.memory
                    elif(chosenCarateristic == ENERGIE):
                        caracteritique = b.energy
                        
                    c = "○"
                    if(tribesON):
                        if(b.tribe == EAU):
                            c = "✿"
                        elif(b.tribe == GLACE):
                            c = "❖"
                        elif(b.tribe == FEU):
                            c = "♣"
                        elif(b.tribe == TERRE):
                            c = "▲"
                    
                    
                    if (deseaseON and grille[(i,j)].bobs[0].sick):
                        print("\033[0;37m", c ,"\033[0;30m", end="") # blanc
                    elif (caracteritique < ((parametreAffichageMin) + 1/4*(parametreAffichageMax-parametreAffichageMin))):
                        print("\033[0;35m", c ,"\033[0;30m", end="") #rose 35
                    elif ((caracteritique < (parametreAffichageMin + 1/2*(parametreAffichageMax-parametreAffichageMin))) and (caracteritique >= (parametreAffichageMin + 1/4*(parametreAffichageMax-parametreAffichageMin)))):
                        print("\033[0;34m", c ,"\033[0;30m", end="") #bleu 34
                    elif ((caracteritique < (parametreAffichageMin + 3/4*(parametreAffichageMax-parametreAffichageMin))) and (caracteritique>= (parametreAffichageMin + 1/2*(parametreAffichageMax-parametreAffichageMin)))):
                        print("\033[0;32m", c ,"\033[0;30m", end="")#vert 32
                    elif (caracteritique >= (parametreAffichageMin + 3/4*(parametreAffichageMax-parametreAffichageMin))):
                        print("\033[0;33m", c ,"\033[0;30m", end="")#jaune 33
                else:
                    print("\033[0;31m ♥ \033[0;30m", end="")
            else:
                print("   ", end="")
        print("|", end="")
        print("")
    for a in range(M // 2 * 3):
        print(" _", end="")
    print("\n")
    
    sleep(sleepTime)

def afficheGrilleSimpleCouleurEducation(tick, day): #pourrait être adapté à d'autres booleean
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
    kindnessMoy = avgKindness()
    kindnessMax = maxKindness()
    kindnessMin = minKindness()
    
    nbmalade = nbBobs_malade()
    longevityMoy = avgLongevity()
    
    print("\033[H\033[J", end="")

    print("Jour : ",day,"Tic : ",tick)
    print("Nombre de bob vivant : ",len(allBobs),"  Nombre de bobs morts : ",len(deadBobs))
    print("Nombre de Bob malade :", nbmalade, "Age moyen :", longevityMoy, "Nombre de bob éduqués : ",nbBobs_educated())
    print("Energie moyenne : ",trunc(energieMoy*1000)/1000,"Energie minimale : ", trunc(energieMin*1000)/1000, "Energie maximum : ",trunc(energieMax*1000)/1000)
    if(speedON):
        print("Vitesse moyenne : ",trunc(vitesseMoy*1000)/1000,"Vitesse minimale : ", trunc(vitesseMin*1000)/1000, "Vitesse maximum : ",trunc(vitesseMax*1000)/1000)
    if(massON):
        print("Masse moyenne : ",trunc(masseMoy*1000)/1000,"Masse minimale : ", trunc(masseMin*1000)/1000, "Masse maximum : ",trunc(masseMax*1000)/1000)
    if(perceptionON):
        print("Perception moyenne : ",trunc(perceptionMoy*1000)/1000,"Perception minimale : ", trunc(perceptionMin*1000)/1000, "Perception maximum : ",trunc(perceptionMax*1000)/1000)
    if(memoryON):
        print("Mémoire moyenne : ",trunc(memoireMoy*1000)/1000,"Mémoire minimale : ", trunc(memoireMin*1000)/1000, "Mémoire maximum : ",trunc(memoireMax*1000)/1000)
    if(kindnessON):
        print("Gentillesse moyenne : ",trunc(kindnessMoy*1000)/1000,"Mémoire minimale : ", trunc(kindnessMin*1000)/1000, "Mémoire maximum : ",trunc(kindnessMax*1000)/1000)


    for a in range(M // 2 * 3):
        print(" _", end="")
    print("")
    for i in range(N):
        print("|", end="")
        for j in range(M):
            if ((i, j) in grille):
                if (grille[(i, j)].bobs != []):
                    b = grille[(i, j)].bobs[0]
                    caracteristique = b.educated
                        
                    c = "○"
                    if(tribesON):
                        if(b.tribe == EAU):
                            c = "✿"
                        elif(b.tribe == GLACE):
                            c = "❖"
                        elif(b.tribe == FEU):
                            c = "♣"
                        elif(b.tribe == TERRE):
                            c = "▲"
                    
                    if (deseaseON and grille[(i,j)].bobs[0].sick):
                        print("\033[0;37m", c ,"\033[0;30m", end="") # blanc
                    elif (caracteristique):
                        print("\033[0;35m", c ,"\033[0;30m", end="") #rose 35
                    else:
                        print("\033[0;34m", c ,"\033[0;30m", end="") #bleu 34
                else:
                    print("\033[0;31m ♥ \033[0;30m", end="")
            else:
                print("   ", end="")
        print("|", end="")
        print("")
    for a in range(M // 2 * 3):
        print(" _", end="")
    print("\n")
    sleep(0.20)


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
