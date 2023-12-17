"""
Ce fichier contient la classe Nourriture

La classe nourriture sera surmement remplacée par une simple fonction qui met une quantité de nourriture dans des cases

Une nourriture est définie par :
-ses coordonnee : un tuple (x,y) coordonnee
-la case dans laquelle la nourriture est : case
-une quantité de nouriture : energy

"""

__date__ = "2030-12-10"

from case import Case
from random import *
from parametre import *


def ajouterNourritureGrille(nombreNourriture=numberFood, energieNourriture=foodE):
    for i in range(nombreNourriture):
        ajouterNourritureCase(energieNourriture)


def ajouterNourritureCase(energieNourriture=foodE):
    coord = (randint(0, N - 1), randint(0, N - 1));

    if (coord not in grille):
        case = Case(coord)
        case.ajouterNourriture(energieNourriture)
    else:
        case = grille[coord]
        case.ajouterNourriture(energieNourriture)


def viderNourritureGrille():
    caseSuprCoord = []
    for c in grille:
        grille[c].viderNourriture()
        if (grille[c].estVide()):
            caseSuprCoord.append(c)
        for cSupr in caseSuprCoord:  # on est obligés de supprimer après vu qu'on peut pas modifier un dictionnaire en même temps qu'on le parcourt
            grille[cSupr].supprimer()


def renouvellerNourriture(nombreNourriture=numberFood, energieNourriture=foodE):
    viderNourritureGrille()
    ajouterNourritureGrille(nombreNourriture, energieNourriture)