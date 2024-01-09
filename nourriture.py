from case import Case
from random import *
from parametre import *

def ajouterNourritureGrille(nombreNourriture = numberFood, energieNourriture = foodE):
    for i in range (nombreNourriture) :
        ajouterNourritureCase(energieNourriture)

def ajouterNourritureCase(energieNourriture = foodE):
    coord = (randint(0,N-1),randint(0,N-1))
    
    if(coord not in grille):
        case = Case(coord)
        case.ajouterNourriture(energieNourriture)
    else :
        case = grille[coord]
        case.ajouterNourriture(energieNourriture)

def ajouterNourritureCaseSpecifique(coordCase, qtite_nourriture = foodE):
        if(coordCase not in grille):
            Case(coord = coordCase, qtite_nourriture = qtite_nourriture)
        else :
            grille[coordCase].qtite_nourriture += qtite_nourriture
#la fonction ajouterNourriture pour une case est dans case.py

def viderNourritureGrille():
    caseSuprCoord = []
    for c in grille:
        grille[c].viderNourriture()
        if (grille[c].estVide()):
            caseSuprCoord.append(c)
    for cSupr in caseSuprCoord: #on est obligés de supprimer après vu qu'on peut pas modifier un dictionnaire en même temps qu'on le parcourt
        grille[cSupr].supprimer()

def renouvellerNourriture(nombreNourriture = numberFood, energieNourriture = foodE) :
    viderNourritureGrille()
    ajouterNourritureGrille(nombreNourriture, energieNourriture)