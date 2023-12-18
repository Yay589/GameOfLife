"""
Ce fichier defini la classe Case

Une case contient :
-liste de bobs : bobs
-une quantité de nouriture : qtite_nourriture

"""
__date__ = "2030-12-10"

from parametre import *

class Case():
    def __init__(self, coord, liste_bobs=None, qtite_nourriture=0):
        self.coordonnee = coord
        if (liste_bobs is None):
            self.bobs = []
        else:
            self.bobs = liste_bobs
        self.qtite_nourriture = qtite_nourriture
        grille[coord] = self

    def ajouterBob(self, bob):
        self.bobs.append(bob)

    def enleverBob(self, bob):
        bobIndex = self.bobs.index(bob)
        del (self.bobs[bobIndex])
        # si il a plus rien on enleve la case du dictionnaire
        self.supprimer()

    def ajouterNourriture(self, qtite_nourriture):
        self.qtite_nourriture += qtite_nourriture

    def viderNourriture(self):
        self.qtite_nourriture = 0

    def estVide(self):
        return ((self.qtite_nourriture == 0) and ((self.bobs == []) or (self.bobs == None)))

    def supprimer(self):
        if (self.estVide()):
            del grille[self.coordonnee]

    def speak(self):
        print("(Case) Je suis en : ", self.coordonnee, ", je contiens : " \
              , len(self.bobs), " bobs. Et : ", self.qtite_nourriture, "point de nourriture \n")
