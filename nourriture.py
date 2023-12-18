<<<<<<< HEAD
from case import Case
from random import *
from parametre import *

class Nourriture():
    #objet nourriture prend en paramètre optionnel la quantié d'énergie (par défaut = qtité définie dans parametre)
    def __init__(self,foodEnergy = foodE, coord = (randint(0,N-1),randint(0,N-1))):
        self.energy = foodEnergy
        self.coordonnee = coord
        if(coord not in grille):
            self.case = Case(coord,qtite_nourriture = self.energy)
            grille[coord] = self.case
        else:
            self.case = grille[coord]
            self.case.ajouterNourriture(self.energy)

    def speak(self): #juste pour faire des tests
        print("(Food) Je suis en : ",self.coordonnee, "J'ai",self.energy,"energie")
=======
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
>>>>>>> 43d1b1af36d40a2d7c831b23dc6985cf2aa5a9c6
