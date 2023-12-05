<<<<<<< HEAD
from parametre import *

class Case():
    def __init__(self, coord, liste_bobs = None, qtite_nourriture = 0 ):
        self.coordonnee = coord
        if(liste_bobs is None):
            self.bobs = []
        else:
            self.bobs = liste_bobs
        self.qtite_nourriture = qtite_nourriture
    def ajouterBob(self,bob):
        self.bobs.append(bob)
        
    def enleverBob(self,bob):
        bobIndex = self.bobs.index(bob)
        del(self.bobs[bobIndex])
        
        #si il a plus rien on enleve la case du dictionnaire
        self.supprimer()

    def ajouterNourriture(self,qtite_nourriture):
        self.qtite_nourriture += qtite_nourriture
        
    def viderNourriture(self):
        self.qtite_nourriture = 0
    
    def estVide(self):
        return ((self.qtite_nourriture == 0) and ((self.bobs == []) or (self.bobs == None)))
        
    def supprimer(self):
        if(self.estVide()):
            del grille[self.coordonnee]
    
    def speak(self):
=======
from parametre import *

class Case():
    def __init__(self, coord, liste_bobs = None, qtite_nourriture = 0 ):
        self.coordonnee = coord
        if(liste_bobs is None):
            self.bobs = []
        else:
            self.bobs = liste_bobs
        self.qtite_nourriture = qtite_nourriture
    def ajouterBob(self,bob):
        self.bobs.append(bob)
        
    def enleverBob(self,bob):
        bobIndex = self.bobs.index(bob)
        del(self.bobs[bobIndex])
        
        #si il a plus rien on enleve la case du dictionnaire
        self.supprimer()

    def ajouterNourriture(self,qtite_nourriture):
        self.qtite_nourriture += qtite_nourriture
        
    def viderNourriture(self):
        self.qtite_nourriture = 0
    
    def estVide(self):
        return ((self.qtite_nourriture == 0) and ((self.bobs == []) or (self.bobs == None)))
        
    def supprimer(self):
        if(self.estVide()):
            del grille[self.coordonnee]
    
    def speak(self):
>>>>>>> bb52c2c6c99675430ca25acece2616dfd70ed219
        print("(Case) Je suis en : ",self.coordonnee, ", je contiens : ",len(self.bobs)," bobs. Et : ",self.qtite_nourriture,"point de nourriture \n")