from parametre import*
from nourriture import*

class Case():
    def __int__(self, coord, liste_bobs = [], qtite_nourriture = 0 ):
        #pourquoi pas mettre des sets à la place de listes
        self.coordonnee
        self.bobs = liste_bobs
        self.qtite_nourriture = Nourriture()
    def ajouterBob(self,bob):
        self.bobs = self.bobs + [bob]

    def ajouterNourriture(self,nourriture):
        self.qtite_nourriture += nourriture