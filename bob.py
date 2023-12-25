"""
Ce fichier contient la classe Bob :

Un bob est defini par :
-ses coordonnee : un tuple (x,y) coordonnee
-la case dans laquelle il est : case
-sa quantité d'energie : energy
-sa vitesse : speed
-sa masse : mass

-un booleen qui indique s'il est mort : dead
-un booleen qui indique s'il vient de naître : birthDay

-un buffer pour gerer les deplacement quand la vitesse est pas entière : speedBuffer

"""

__authors__ = ("Célestine")
__date__ = "2030-12-10" #10 decembre
__version__= "1.0" 

from random import *
from parametre import *
from case import Case
from math import trunc


class Bob():
    def __init__(self, birthDay = 0, 
                 bobEnergy = bobSpawnE, 
                 bobSpeed = bobS, 
                 bobMass = bobM, 
                 bobPerception = bobP, 
                 bobMemory = bobMem,
                 coord = (randint(0,N-1),randint(0,N-1)) ) :
        self.coordonnee = coord #avec randint les deux bornes sont inclusives
        if(coord not in grille):
            self.case = Case(coord)
            self.case.ajouterBob(self)
        else :
            self.case = grille[coord]
            self.case.ajouterBob(self) #on ajoute un bob a la liste de bob de la case de clé coord
        self.birthDay = birthDay
        self.dead = 0
        self.speedBuffer = 0

        self.energy = bobEnergy
        self.speed = bobSpeed
        self.mass = bobMass
        self.perception = bobPerception
        self.memory = bobMemory
        
        self.nourritureEnVue = []
        self.coordNourriturePref = None

    def mourir(self):
        self.dead = 1 #jsp si on doit verifier si le bob à plus d'énergie
        deadBobs.append(self)
        bobIndex = allBobs.index(self)
        del(allBobs[bobIndex])

    #reproduction solo, renvoie 0 si le bob n'a pas assez d'énrgie et 1 si le bob fait un bébé
    def reproduction(self):
        """
        Cette fonction
        -verifie le niveau d'energie du parent
        -créer un bébé bob (dans la liste de nos bobs)
        -met à jour le niveau d'energie du parent

        Valeur de retour : la fonction renvoie 1 si le bob à assez
        d'energie pour faire un bébé et renvoie 0 s'il n'y a pas de bob
        créé.
        """
        if(self.energy == bobMaxE):
            vitesseBebe = self.speed + random()%0.2 - 0.1
            perceptionBebe = max((self.perception + randint(-1,1)),0) #a tester pour verifier si ça marche
            memoireBebe = self.memory + randint(-1,1)
            print(self.perception, perceptionBebe, memoireBebe)
            allBobs.append(Bob(birthDay = 1, bobEnergy = bobBirthE, bobSpeed = vitesseBebe, bobPerception = perceptionBebe, bobMemory = memoireBebe, coord = self.coordonnee))
            self.energy -= bobLaborE
            return 1
        else:
            #print("no baby")
            return 0
       
#deplacement :
    #gere le buffer de vitesse et renvoie le nombre de case que devra parcourir le bob
    def calculNbCasesDeplacement(self):
        #3 premières lignes pour gérer le buffer vitesse
        nombreCasesFloat = self.speed + self.speedBuffer  #ajoute le buffer au nombre de cases à parcourir
        nombreCasesInt = trunc(nombreCasesFloat) #donne le nombre entier de cases
        self.speedBuffer = nombreCasesFloat - nombreCasesInt #calcule le nouveau buffer
        return nombreCasesInt
    
    #modifie les coordonnée d'un bob pour le deplacer aléatoirement du bon nombre de case    
    def calculNouvellesCoordonneeDeplacement(self):
        for i in range(self.calculNbCasesDeplacement()): #une itération par case à bouger
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
    
    #met le bob dans sa nouvelle case
    def deplacerBobCoordonnee(self):
        if(self.coordonnee not in grille):
            self.case = Case(self.coordonnee) #on créer une case
            self.case.ajouterBob(self) #on ajoute un bob a cette case
            grille[self.coordonnee] = self.case #on ajoute la nouvelle case a notre grille
        else :
            self.case = grille[self.coordonnee]
            grille[self.coordonnee].ajouterBob(self) #on ajoute un bob a la liste de bob de la case de clé coord
        
    def perdreEnergieDeplacement(self):
        energyLoss = max(((self.speed)**2 * self.mass + 1/5*self.perception),0.5)
        self.energy -= energyLoss #il faudra adapter ça pour les prochaines versions
    
    #le bob se deplace aléatoirement
    def bouger(self):
        """
        Cette fonction
        -retire le bob de sa case actuelle
        -calcule ses nouvelles coordonnées en fonction de la vitesse et
        du speedBuffer de ce bob.
        -modifie les coordonnées et ajoute le bob dans la bonne case
        -calcule et met à jour le niveau d'energie du bob
        -"tue" le bob s'il n'a plus d'energie

        Gestion des erreurs :
        Si le bob est mort ou vient de naître la fonction renvoie -1
        """
        if(self.dead == 1):
            print("Attention ce bob est mort")
            return -1
        if(self.birthDay == 1):
            self.birthDay = 0
            #print("This bob just apeared, wait till the next tic")
            return -1

        #pour diminuer son niveau d'énergie
        self.perdreEnergieDeplacement()

        if(self.energy <= 0):
            self.mourir()
            return -1
        
        self.case.enleverBob(self)
        
        # pour faire bouger le bob d'autant de cases que nécessaire
        self.calculNouvellesCoordonneeDeplacement()
        
        #changement de case
        self.deplacerBobCoordonnee()
        return 0
    
#perception
    #renvoie une liste qui contient les tuples des coordonnée adjactente à la case du bob
    def coordAdjacentes(self):
        x = self.coordonnee[0]
        y = self.coordonnee[1]
        coordonneeAdjacentes = [(self.coordonnee)] #liste de tuples
        for i in range(0,self.perception+2):
            for j in range(0,self.perception-i+1):
            #peut être ajouter une verification que ca peut bien être dans la grille en terme de coordonnee
                if(i==0):
                    coordonneeAdjacentes.append((x,y+j))
                    coordonneeAdjacentes.append((x,y-j))
                elif(j==0):
                    coordonneeAdjacentes.append((x+i,y))
                    coordonneeAdjacentes.append((x-i,y))
                else :
                    coordonneeAdjacentes.append((x+i,y+j))
                    coordonneeAdjacentes.append((x+i,y-j))
                    coordonneeAdjacentes.append((x-i,y+j))
                    coordonneeAdjacentes.append((x-i,y-j))
        return coordonneeAdjacentes
 
    #met a jour la liste de nourriture en vue du bob, renvoie le nombre de nourritures vues
    #peut être mieux de juste renoyer la liste comme ça les bobs aurait pas besoin de s'en souvenir
    def setNourritureEnVue(self): #renvoie le nombre de nourriture
        x = self.coordonnee[0]
        y = self.coordonnee[1]
        
        #mise à jour de la liste de nourriture
        self.nourritureEnVue = [] #on vide la liste de tuple
        
        for coord in self.coordAdjacentes() :
            if (coord in grille):
                if (grille[coord].qtite_nourriture != 0):
                    print("Le bob voit une nourriture")
                    self.nourritureEnVue.append(coord)
        return len(self.nourritureEnVue)
    
    #renvoie la distance entre un bob et des coordonnées
    def distance(self, coord):#pourrait très bien ne pas être dans le classe bob
        return abs(coord[0] - self.coordonnee[0]) + abs(coord[1] - self.coordonnee[1])
    
    #definie la nourriture préférée du bob
    def setNourriturePreferee(self):
        if(len(self.nourritureEnVue)==0):
            print("Erreur, pas de nourriture en vue")
            return -1
        min = self.distance(self.nourritureEnVue[0])
        coordPref = self.nourritureEnVue[0]
        for i in range(1,len(self.nourritureEnVue)):
            coordN = self.nourritureEnVue[i]
            if (self.distance(coordN)< min):
                coordPref = coordN
            elif ((self.distance(coordN) == min) and (grille[coordN].qtite_nourriture > grille[coordPref].qtite_nourriture)):
                coordPref = coordN
        self.coordNourriturePref = coordPref       

    #se deplace de manière optimiser mais aléatoire vers les coordonnées données
    def beeline(self,coordCible): #déplacement en zigzag vers une cible
        if(self.coordonnee == coordCible):
            print("Le bob est déjà sur cette case")
            return -1
        self.case.enleverBob(self)
        x = coordCible[0] - self.coordonnee[0] 
        y = coordCible[1] - self.coordonnee[1]
        nbCase = self.calculNbCasesDeplacement()
        
        self.perdreEnergieDeplacement()
        
        if(nbCase >= self.distance(coordCible)):
            self.coordonnee = coordCible
        
        else :
            for i in range(nbCase):
                if(x == 0):
                    if(y>0):
                        self.coordonnee = (self.coordonnee[0],self.coordonnee[1]+nbCase)
                    else:
                        self.coordonnee = (self.coordonnee[0],self.coordonnee[1]-nbCase)
    
                elif(y == 0):
                    if(x>0):
                        self.coordonnee = (self.coordonnee[0]+nbCase,self.coordonnee[1])
                    else:
                        self.coordonnee = (self.coordonnee[0]-nbCase,self.coordonnee[1])
    
                else:
                    choix = randint(0,1)
                    if (choix):
                        if(x>0):
                            self.coordonnee = (self.coordonnee[0]+1,self.coordonnee[1])
                        else:
                            self.coordonnee = (self.coordonnee[0]-1,self.coordonnee[1])
                    else:
                        if(y>0):
                            self.coordonnee = (self.coordonnee[0],self.coordonnee[1]+1)
                        else:
                            self.coordonnee = (self.coordonnee[0]-1,self.coordonnee[1]-1)
        self.deplacerBobCoordonnee()  
        return 0      
    
#manger
    #renvoie 0 si le bob n'a rien à manger sur sa case et 1 si le bob a mangé
    def manger(self):
        """
        Cette fonction
        -calcule la quantité d'energie que le bob peut manger
        -met a jour l'energie du bob et qui reste dans la case

        Valeur de retour : cette fonction renvoie 1 si le bob à mangé,
        0 s'il n'y avait rien a manger dans la case et -1 si erreur

        Gestion des erreurs :
        La fonction renvoie -1 si le bob vient de naître ou est mort
        """
        if(self.birthDay == 1 or self.dead == 1):
            self.birthDay = 0
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

    #indique si deux bobs partagent une même case, pas sure que cette fonction soit utile.
    def memeCase(self, b):
        if(self.coordonnee == b.coordonnee): return 1
        else : return 0
    
    #indique si un bob est seul sur sa case
    def seul(self):
            #version si les bobs stockent leur case
        #return len(self.case.bobs)==1 #si la taille de la liste de bob de sa case est 1 il est seul
            #version si on dit que les bobs ne sockent plus leur case :
        return len(grille[self.coordonnee].bobs) == 1
    
    #choisi un bob parmis ceux qui sont sur la même case
    #cette fonction est inutile vu qu'on va remelanger le dict plutôt
    def choisirUnBob(self): #peut être mieux de mettre ça dans case.py jsp
        n = len(grille[self.coordonnee].bobs)
        indexBobChoisi = randint(0,n-1)
        return indexBobChoisi
    
#les deux fonctions suivante enfaite c'est Huy qui fait ça
    def enDanger(self):
        #si le bob voit un prédateur la fonction renvoie un
        return -1
    #renvoie 1 si le bob à besoin de se proteger (et fait le nécessaire) et 0 si le bob n'est pas en danger
    def seProteger(self):
        if(self.enDanger):
            #le bob fait une action pour se proteger
            return 1
        else : return 0
    
#fonction de communication
    #le bob printf ses coordonnee et son energie
    def speak(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordonnee, "J'ai",self.energy,"energie")
    
    #le bob printf ses coordonnee, sa vitesse et son energie
    def speakSpeed(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordonnee,"J'ai une vitesse de ",self.speed, "J'ai",self.energy,"energie")

    #le bob print coord, vitesse, preception
    def speakPerception(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordonnee,"J'ai une vitesse de ",self.speed, "J'ai une preception de ",self.perception, "J'ai",self.energy,"energie")
