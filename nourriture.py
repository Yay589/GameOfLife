from case import Case
from random import *
from parametre import *


class Nourriture():
    # objet nourriture prend en paramètre optionnel la quantié d'énergie (par défaut = qtité définie dans parametre)
    def __init__(self, FoodEnergy=FoodE, coord=(randint(0, 100), randint(0, 100))):
        self.energy = FoodEnergy
        self.coordonnee = coord
        if (coord not in grille):
            self.case = Case(coord, qtite_nourriture=100)
        else:
            grille(coord).ajouterNourriture(self)

    # a prioris plus besoin de ces fonctions si la qtité de nourriture est stockée direct dans les cases
    def diminuer(self, quantite):
        # cette fonction a pour but de pouvoir adapter la taille d'une nourriture en fonction de sa quantité d'énergie
        self.energy -= quantite

    def disparaitre(self):
        # pour supprimer la nourriture quand il n'y a plus d'énergie
        self.energy = 0
        # faire disparaitre graphiquement la nourriture
        # ou la faire disparaitre si on la stocke dans une liste ou je sais pas quoi

    def speak(self):  # juste pour faire des tests
        print("Je suis en : ", self.coordonnee, "J'ai", self.energy, "energie")