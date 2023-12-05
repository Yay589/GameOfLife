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
=======
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
>>>>>>> bb52c2c6c99675430ca25acece2616dfd70ed219
        print("(Food) Je suis en : ",self.coordonnee, "J'ai",self.energy,"energie")