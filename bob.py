<<<<<<< HEAD
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
=======
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
__date__ = "2030-12-10"


from random import *
from parametre import *
from case import Case
from math import trunc


class Bob():
    def __init__(self, birthDay = 0, bobEnergy = bobSpawnE, bobSpeed = bobS, bobMass = bobM, coord = (randint(0,N-1),randint(0,N-1)) ) :
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

    def mourir(self):
        self.dead = 1
        deadBobs.append(self)
        bobIndex = allBobs.index(self)
        del(allBobs[bobIndex])

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
            allBobs.append(Bob(birthDay = 1, bobEnergy = bobBirthE, bobSpeed = vitesseBebe, coord = self.coordonnee))
            self.energy -= bobLaborE
            return 1
        else:
            #print("no baby")
            return 0

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

        self.case.enleverBob(self)

        #3 premières lignes pour gérer le buffer vitesse
        nombreCasesFloat = self.speed + self.speedBuffer  #ajoute le buffer au nombre de cases à parcourir
        nombreCasesInt = trunc(nombreCasesFloat) #donne le nombre entier de cases
        self.speedBuffer = nombreCasesFloat - nombreCasesInt #calcule le nouveau buffer
        #pour diminuer son niveau d'énergie
        energyLoss = max(((self.speed)**2 * self.mass),0.5)
        self.energy -= energyLoss #il faudra adapter ça pour les prochaines versions

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

    def speak(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordonnee, "J'ai",self.energy,"energie")

    def speakSpeed(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordonnee,"J'ai une vitesse de ",self.speed, "J'ai",self.energy,"energie")
>>>>>>> 43d1b1af36d40a2d7c831b23dc6985cf2aa5a9c6
