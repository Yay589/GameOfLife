from random import *
from case import Case
from parametre import *
from math import trunc

class Bob():
    def __init__(self, BobEnergy = BobSpawnE, BobSpeed = BobS, BobMass = BobM, coord = (randint(0,100),randint(0,100)) ) :
        self.coordonnee = coord #avec randint les deux bornes sont inclusives
        if(coord not in grille):
            self.case = Case(coord) #on créer une case
            Case.ajouterBob(self) #on ajoute un bob a cette case
            #self.case.list_bob.append(self) #on met un bob dans la list de bob de cette case
        else :
            grille[coord].ajouterBob(self) #on ajoute un bob a la liste de bob de la case de clé coord
        self.dead = 0
        self.speedBuffer = 0

        #Pas nécessaire, c'est juste si on veut pouvoir modifier certain paramètres
        self.energy = BobEnergy
        self.speed = BobSpeed
        self.mass = BobMass

    def speak(self): #juste pour faire des tests
        print("Je suis en : ",self.coordonnee, "J'ai",self.energy,"energie")
    def isDead(self): #je suis pas sure que ça soit utile
        return self.dead
    def bouger(self):
        #3 premières lignes pour gérer le buffer vitesse
        nombreCasesFloat = self.speed + self.speedBuffer  #ajoute le buffer au nombre de cases à parcourir
        nombreCasesInt = trunc(nombreCasesFloat) #donne le nombre entier de cases
        self.speedBuffer = nombreCasesFloat - nombreCasesInt #calcule le nouveau buffer
        #pour diminuer son niveau d'énergie
        self.energy -= (self.speed)**2 * self.mass #il faudra adapter ça pour les prochaines versions !!
        # pour faire bouger le bob d'autant de cases que nécessaire
        for i in range(nombreCasesInt): #une itération par case à bouger
            boucle = True #permet de faire un équivalent de do(changer de coord) while (nouvelles coordonnées pas dans la grille)
            while boucle :
                a = randint(1,2) #on modifie soit x soit y
                b = randint(1, 2) #on modifie de -1 ou +1
                if a == 1:
                    if b == 1 :
                        x = self.coordonnee[0] + 1
                    elif b == 2 :
                        x = self.coordonnee[0] - 1
                    if (x<=100 and x>=0): #on vérifie que le bob ne s'échappe pas de la grille
                        self.coordonnee[0] = x
                        boucle = False
                elif a == 2:
                    if b == 1 :
                        y = self.coordonnee[1] + 1
                    elif b == 2 :
                        y = self.coordonnee[1] - 1
                    if (y<=100 and y>=0):
                        self.coordonnee[1] = y
                        boucle = False
        self.Case

    def manger(self,nourriture): #il faut déjà avoir verifier que le bob est sur une case nourriture et avoir choisi un bob s'il en a plusieur
        faim = BobMaxE - self.energy
        reste = nourriture.energy - faim
        if reste <= 0 :
            nourriture.disparaitre
            self.energy += nourriture.energy
        else :
            nourriture.diminuer(faim)  #on enleve à la nourriture l'énergie que le bob consomme
            self.energy = BobMaxE