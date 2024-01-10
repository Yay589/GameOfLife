"""
Ce fichier contient les fonctions qui permettent de faire un affichage terminal pour notre jeu

3 affichages differents disponible

"""

__date__ = "2023-10-12"


from parametre import *
from nourriture import *
from case import Case
from bob import Bob


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
