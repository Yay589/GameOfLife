from random import *
from parametre import *
from case import Case
from math import trunc
    

class Bob():
    def __init__(self, birthDay = 0, bobEnergy = bobSpawnE, bobSpeed = bobS, bobMass = bobM, coord = (randint(0,N-1),randint(0,N-1)) ) :
        self.coordonnee = coord #avec randint les deux bornes sont inclusives
        if(coord not in grille): # attention il y a un probleme de logique, tous les bobs se mettent dans la même case...
            self.case = Case(coord) #on veux créer une case mais en vrais ça modifie juste les coordonnées : a modifier
            self.case.ajouterBob(self) #on ajoute un bob a cette case
            grille[coord] = self.case
        else :
            self.case = grille[coord]
            self.case.ajouterBob(self) #on ajoute un bob a la liste de bob de la case de clé coord
        self.birthDay = birthDay
        self.dead = 0
        self.speedBuffer = 0

        #Pas nécessaire, c'est juste si on veut pouvoir modifier certain paramètres
        self.energy = bobEnergy
        self.speed = bobSpeed
        self.mass = bobMass
        

    def speak(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordonnee, "J'ai",self.energy,"energie")
    
    def speakSpeed(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordonnee,"J'ai une vitesse de ",self.speed, "J'ai",self.energy,"energie")
        
    
    
    def mourir(self):
        self.dead = 1
        deadBobs.append(self)
        bobIndex = allBobs.index(self)
        del(allBobs[bobIndex])
    
    def reproduction(self):
        if(self.energy == bobMaxE):
            #print("je fais un bebe")
            vitesseBebe = self.speed + random()%0.2 - 0.1
            allBobs.append(Bob(birthDay = 1, bobEnergy = bobBirthE, bobSpeed = vitesseBebe, coord = self.coordonnee))
            self.energy -= bobLaborE
            #allBobs[-1].speakSpeed()
            return 1
        else:
            #print("no baby")
            return 0

        
        
    
    def bouger(self):
        if(self.dead == 1):
            print("Attention ce bob est mort")
            return -1
        if(self.birthDay == 1):
            self.birthDay = 0
            #print("This bob just apeared, wait till the next tic")
            return -1
        
        self.case.enleverBob(self)
            
        #3 premières lignes pour gérer le buffer vitesse
        nombreCasesFloat = self.speed + self.speedBuffer  #ajoute le buffer au nombre de cases à parcourir
        nombreCasesInt = trunc(nombreCasesFloat) #donne le nombre entier de cases
        #self.speakSpeed()
        #print("Je bouge de : ",nombreCasesInt)
        self.speedBuffer = nombreCasesFloat - nombreCasesInt #calcule le nouveau buffer
        #pour diminuer son niveau d'énergie
        energyLoss = max(((self.speed)**2 * self.mass),0.5)
        self.energy -= energyLoss #il faudra adapter ça pour les prochaines versions !!
        
        if(self.energy <= 0):
            self.mourir()
            return -1
        
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
                    if (x<=N-1 and x>=0): #on vérifie que le bob ne s'échappe pas de la grille
                        self.coordonnee = (x,self.coordonnee[1])
                        boucle = False
                elif a == 2:
                    if b == 1 :
                        y = self.coordonnee[1] + 1
                    elif b == 2 :
                        y = self.coordonnee[1] - 1
                    if (y<=N-1 and y>=0):
                        self.coordonnee = (self.coordonnee[0],y)
                        boucle = False
        #changement de case
            
        if(self.coordonnee not in grille): 
            self.case = Case(self.coordonnee) #on créer une case
            self.case.ajouterBob(self) #on ajoute un bob a cette case
            grille[self.coordonnee] = self.case #on ajoute la nouvelle case a notre grille
        else :
            self.case = grille[self.coordonnee]
            grille[self.coordonnee].ajouterBob(self) #on ajoute un bob a la liste de bob de la case de clé coord
        return 0

            
    def manger(self): #renvoie 0 si le bob n'a rien mangé
        #on verifie que le bob ne vient pas de naître
        if(self.birthDay == 1):
            self.birthDay = 0
            #print("This bob just apeared, wait till the next tic")
            return -1   
            
        if(self.case.qtite_nourriture != 0):
            self.energy -= 0.5
            #print("J'ai de la nourriture sur ma case \n")
            faim = bobMaxE - self.energy
            reste = self.case.qtite_nourriture - faim
            #print("j'ai faim de : ",faim, ", reste : ", reste)
            if (reste <= 0) :
                self.energy += self.case.qtite_nourriture
                self.case.qtite_nourriture = 0
            else :
                self.case.qtite_nourriture -= faim  #on enleve à la nourriture l'énergie que le bob consomme
                self.energy = bobMaxE
            return 1
        else :
            #print("il n'y a rien a manger ici \n")
            return 0
