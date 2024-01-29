from parametre import *

"""
Ce fichier defini la classe Case

Une case contient :
-liste de bobs : bobs
-une quantité de nouriture : qtite_nourriture

"""

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
        #print ("self.bobs = ",self.bobs)
        self.bobs.append(bob)

    def enleverBob(self, bob):
        bobIndex = self.bobs.index(bob)
        del (self.bobs[bobIndex])
        # si il a plus rien on enleve la case du dictionnaire
        self.supprimer() #a enlever si on enlevela liste de bob et qu'on a un dictionnaire temporaire plutôt
    
    def ajouterNourriture(self, qtite_nourriture = foodE):
        self.qtite_nourriture += qtite_nourriture

    def viderNourriture(self):
        self.qtite_nourriture = 0

    def estVide(self):
        return ((self.qtite_nourriture == 0) and ((self.bobs == []) or (self.bobs == None)))

    def supprimer(self):
        if (self.estVide()): #eventuellement faire le test avant d'appeller supprimer et là renvoyer une erreur si le test à pas validé
            del grille[self.coordonnee] #on enleve de la grille
            self = None #on oublie l'objet pour le supprimer de la mémoire

    def speak(self):
        print("(Case) Je suis en : ", self.coordonnee, ", je contiens : " \
              , len(self.bobs), " bobs. Et : ", self.qtite_nourriture, "point de nourriture \n")
        