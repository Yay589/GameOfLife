"""
Ce fichier contient la classe Bob :

Un bob est defini par :
-ses coordonnee : un tuple (x,y) coordonnee
-la case dans laquelle il est : case
-sa quantité d'energie : energy
-sa vitesse : speed
-sa masse : mass

-un booleen qui indique s'il est mort : dead
-un booleen qui indique si le bob à le droit de jouer à ce tour : skipingTurn 

-un buffer pour gerer les deplacement quand la vitesse est pas entière : speedBuffer

"""

__date__ = "2024-01-27" #10/01/27
__version__= "2.1" 

from random import *
from parametre import *
from case import Case
from math import trunc


class Bob():
#Fonction qui devraient être utilisées dans le reste du programme :
#########################################################################################
    #Toutes les fonctions (sauf déplacement) renvoient False si elle ne font rien et True si elles font l'action correpondante
    def avantUnTour(self):
        if(deseaseON and self.sick):
            self.sickTicsLeft -= 1
            if(self.sickTicsLeft <= 0):
                self.sick = False
        self.age += 1
    
    def dejaJoue(self):
        if(self.skipingTurn):
            self.skipingTurn = False
            return True
        else:
            return False
    
    #renvoie True si le bob à besoin de se proteger (et fait le nécessaire) et False si le bob n'est pas en danger
    def seProteger(self):
        if(perceptionON and massON and self.enDanger() and self.fuire(self.coordClosestPredator)):
            return True
        else : 
            return False
    
    #reproduction solo
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
        if(soloReproductionON and self.energy == bobMaxE):
            self.previousCoordinates = self.coordinates #met a jour coordonnee precedente
            
            #valeurs de base
            vitesseBebe = bobS
            perceptionBebe = bobP
            memoireBebe = bobMem
            massBebe = bobM
            tribueBebe = -1 #si tribue désactivé -> TO DO : peut etre mettre à 1 et dire que si y'a pas de tribue c'est équivalent à en avoir une seule grande
            
            #calcul des données héreditaire (si caractéritique activée)
            if(speedON):
                vitesseBebe = max((self.speed + random()%0.2 - 0.1),0)
            if(perceptionON):    
                perceptionBebe = max((self.perception + randint(-1,1)),0)
            if(memoryON):
                memoireBebe = max((self.memory + randint(-1,1)),0)
            if(massON):
                massBebe = max((self.mass + random()), 0)
            if(tribesON):
                tribueBebe = self.tribe
                 
            #creation du bebe
            allBobs.append(Bob(bobTribe = tribueBebe, skiping = True, bobEnergy = bobBirthE, bobSpeed = vitesseBebe, bobPerception = perceptionBebe, bobMemory = memoireBebe, bobMass = massBebe, coord = self.coordinates))
            #perte d'energie
            self.energy -= bobLaborE
            self.previousAction = REPRODUCTION_SOLO
            return True
        else: 
            return False
    
    #reproduction duo   
    def reproductionSexuee(self): #renvoie True si le bob fait un bebe et False sinon
        if((not duoReproductionON) or self.energy < bobMinSexE):  
            return False #pas assez d'energie
        bob = self.partenaireDisponible() #avec x un fonction qui renvoie un bob qui à assez d'energie
        if((not duoReproductionON) or bob==None):
            return False #pas de partenaire dispnnible
        
        #valeurs de base
        vitesseBebe = bobS
        perceptionBebe = bobP
        memoireBebe = bobMem
        massBebe = bobM
        tribueBebe = -1 #si tribue désactivé -> TO DO : peut etre mettre à 1 et dire que si y'a pas de tribue c'est équivalent à en avoir une seule grande

            
        #calcul des données héreditaire (si caractéritique activée)
        if(speedON):
            vitesseBebe = max(((self.speed + bob.speed)/2 + random()%0.2 - 0.1),0)
        if(perceptionON):    
            perceptionBebe = max(((self.perception + bob.perception)/2 + randint(-1,1)),0)
        if(memoryON):
            memoireBebe = max(((self.memory + bob.memory)/2 + randint(-1,1)),0)
        if(massON):
            massBebe = max(((self.mass + bob.mass)/2 + random()), 0)
        if(tribesON):
            tribueBebe = self.tribe
        
        #creation du bebe
        allBobs.append(Bob(skiping = True, bobEnergy = bobSexBirthE, bobSpeed = vitesseBebe, bobPerception = perceptionBebe, bobMemory = memoireBebe, bobMass = massBebe, bobTribe= tribueBebe, coord = self.coordinates))
        #perte d'energie
        self.energy -= bobSexLaborE
        bob.energy -= bobSexLaborE
        bob.skipingTurn = True
        self.previousAction = REPRODUCTION_DUO
        bob.previousAction = REPRODUCTION_DUO
        return True
    
    #manger
    #renvoie 0 si le bob n'a rien à manger sur sa case et 1 si le bob a mangé
    def manger(self):
        """
        Cette fonction
        -calcule la quantité d'energie que le bob peut manger
        -met a jour l'energie du bob et qui reste dans la case

        Valeur de retour : cette fonction renvoie True si le bob à mangé,
        False s'il n'y avait rien a manger dans la case
        """
        # if(self.dead == 1):
        #     return -1
        
        
        if(self.case.qtite_nourriture != 0):
            #Enfaite un bob reste jamais sur une case avec de la nourriture puisque s'il en reste c'est qu'il à full energie et donc il peut faire un bébé
            # if(self.coordinates == self.previousCoordinates):
            #     self.energy -= 0.5 #Un bob peut rester sur une nourriture mais il perd 0,5 energie par tour

            self.previousCoordinates = self.coordinates #mise a jour des coord precedentes
            self.previousAction = MANGER

            #calcul du gain d'energie et energie restante sur la case
            faim = bobMaxE - self.energy
            reste = self.case.qtite_nourriture - faim
            if(deseaseON and randint(0,chancesOfFoodPoisoning) == 1):
                self.sick = True
                self.sickTicsLeft = nbSickTics
            if (reste <= 0) :
                self.energy += self.case.qtite_nourriture
                self.case.qtite_nourriture = 0
            else :
                self.case.qtite_nourriture -= faim  #on enleve à la nourriture l'énergie que le bob consomme
                self.energy = bobMaxE
            return True
        else :
            return False  
    
    #Deplacement - regroupe toutes les fonctions de déplacement
    #permet de deplacer un bob, soit pour chercher de la nourriture, soit aléatoirement  
    def bobDeplacement(self):
        self.previousCoordinates = self.coordinates
        if(not self.chercherNouriture()):
            self.bouger()
            self.previousAction = DEPLACEMENT_ALEATOIRE
        if(memoryON):
            self.setNourritureMemorisee()
            self.setCaseMemorisee()

    def attack(self):
        for bob in allBobs:
            if(self.coordinates == bob.coordinates and self != bob):
                if(self.mass > 1.5*bob.mass):
                    self.mass += 0.5*bob.mass
                    bob.mourir()
                elif(1.5*self.mass < bob.mass):
                    bob.mass += 0.5*self.mass
                    self.mourir()
    
    def attaque(self):
        if(perceptionON and len(grille[self.coordinates].bobs)>= 2):
            for smallBob in (grille[self.coordinates].bobs) :
                if((smallBob != self) and (not tribesON or self.tribe != smallBob.tribe)): #soit tribue desactivé soit pas la même tribue
                    if((self.mass > 1.5*smallBob.mass)):
                        self.energy += 0.5*smallBob.energy*(1-smallBob.mass/self.mass)
                        smallBob.mourir()
                        return True
        return False
    
    def partageEnergie(self):
        if(educationON and self.educated and self.sick):
            return False
        elif(kindnessON and self.kindness>0):
            for coord in self.coordAdjacentes(self.coordinates,1): 
                if coord in grille :
                    for b in grille[coord].bobs:
                        gentillesse = self.kindness
                        if(tribesON):
                            if(self.tribe == b.tribe):
                                gentillesse = (gentillesse*2)%100
                            else:
                                gentillesse = gentillesse / 2
                        if ((b != self) 
                            and self.energy > b.energy
                            and randint(0,101)<= gentillesse):
                            energieTransmise = self.energy - b.energy
                            if(self.kindness > 50):
                                energieTransmise /= 2
                            else:
                                energieTransmise /=4
                            
                            self.energy -= energieTransmise
                            b.energy += energieTransmise
                            b.kindness += kidnessAdded
                            if(self.sick):
                                b.sick = True
                                b.sickTicsLeft = nbSickTics
                            
    def eduquer(self):
        if(educationON and self.educated):
            for coord in self.coordAdjacentes(self.coordinates,1):
                if coord in grille :
                    for b in grille[coord].bobs:
                        if(b.skipingTurn == False and b.educated == False):
                            b.educated = True
                            b.skipingTurn = True
                            return True
        return False
                            
#########################################################################################
    
    #Fonctions internes à ce fichier 
    def __init__(self, 
                 skiping = False, #True si le bob naît d'un autre bob
                 bobEnergy = bobSpawnE, 
                 bobSpeed = bobS, 
                 bobMass = bobM, 
                 bobPerception = bobP, 
                 bobMemory = bobMem,
                 bobTribe = 0,
                 coord = (randint(0,N-1),randint(0,M-1)) ) :
        self.energy = bobEnergy
        #coordonnee
        self.coordinates = coord #avec randint les deux bornes sont inclusives
        
        #pour l'affichage graphique :
        self.previousCoordinates = coord #pour l'instant on va dire ça s'il vient de pop
        self.previousAction = NAITRE
        
        #pour les stat :
        self.age = 0
        
        #ajout du bob dans la grille
        if(coord not in grille):
            self.case = Case(coord)
            self.case.ajouterBob(self)
        else :
            self.case = grille[coord]
            self.case.ajouterBob(self) #on ajoute un bob a la liste de bob de la case de clé coord
        
        #booleans
        self.skipingTurn = skiping #indique si le bob doit sauter ce tour (jour de naissance ou s'il a fait un bebe)
        self.dead = False

        #caracteritiques fixes du bob
        if(randomStartOn):
            self.speed = random() % maxRandomSpeed + 1
            self.mass = random() % maxRandomMass + 1
            self.perception = random() % maxRandomPerception + 1
            self.memory = random() % maxRandomMemory + 1
        else:
            self.speed = bobSpeed
            self.mass = bobMass
            self.perception = bobPerception
            self.memory = bobMemory
        
        #vitesse
        self.speedBuffer = 0
        
        #perecption
        self.seenFoods = []
        self.coordFavouriteFood = None
        self.coordClosestPredator = ()
        self.coordClosestPrey = ()
        
        #memoire
        self.availableMemory = trunc(bobMemory) #pour l'instant aucune case mémoirisé donc memoire dispo = memoire totale
        self.rememberedFoods = {}
        self.rememberedSquares = []
        
        #caractéristique supplémentaire :
        self.kindness = birthKindness
        self.sick = False
        self.sickTicsLeft = 0
        if(bobTribe == 0):
            if(tribesRandom):
                self.tribe = randint(1,4)
            else:
                if(self.coordinates[0]< N/2 and self.coordinates[1]< M/2):
                    self.tribe = 1
                elif(self.coordinates[0]< N/2 and self.coordinates[1]>= M/2):
                    self.tribe = 2
                elif(self.coordinates[0]>= N/2 and self.coordinates[1]< M/2):
                    self.tribe = 3
                elif(self.coordinates[0]>= N/2 and self.coordinates[1]>= M/2):
                    self.tribe = 4
        else:
            self.tribe = bobTribe
        self.educated = False
        if(educationON and randint(1,chancesOfBeingBornEducated)==1):  
            self.educated = True


    def mourir(self):
        self.dead = 1 #jsp si on doit verifier si le bob à plus d'énergie
        deadBobs.append(self)
        bobIndex = allBobs.index(self)
        bobIndexCase = grille[self.coordinates].bobs.index(self)
        grille[self.coordinates].bobs.pop(bobIndexCase)
        del(allBobs[bobIndex])
        if(self.energy <= 0):
            self.previousAction = MOURIR_ENERGIE
        else:
            self.previousAction = MOURIR_ATTAQUE

#deplacement :
    #gere le buffer de vitesse et renvoie le nombre de case que devra parcourir le bob
    def calculNbCasesDeplacement(self):
        #3 premières lignes pour gérer le buffer vitesse
        nombreCasesFloat = self.speed + self.speedBuffer  #ajoute le buffer au nombre de cases à parcourir
        nombreCasesInt = trunc(nombreCasesFloat) #donne le nombre entier de cases
        self.speedBuffer = nombreCasesFloat - nombreCasesInt #calcule le nouveau buffer
        return nombreCasesInt
    
    def caseVisitee(self,coord):
        return (coord in self.rememberedSquares)
    
    #modifie les coordonnée d'un bob pour le deplacer aléatoirement du bon nombre de case    
    def calculNouvellesCoordonneeDeplacement(self):
        i = 0 #compteur pour pas se retrouver bloqué 
        x = self.coordinates[0]
        xBefore = x
        y = self.coordinates[1]
        yBefore = y
        #self.previousCoordinates = self.coordinates #on enregiste les coordonnees precentes avant des les modifier
        for i in range(self.calculNbCasesDeplacement()): #une itération par case à bouger
            boucle = True #permet de faire un équivalent de do(changer de coord) while (nouvelles coordonnées pas dans la grille)
            while boucle :
                i += 1
                a = randint(1,2) #on modifie soit x soit y
                b = randint(1, 2) #on modifie de -1 ou +1
                if a == 1:
                    if b == 1 :
                        x = xBefore + 1
                    elif b == 2 :
                        x = xBefore - 1
                    if (x<=N-1 and x>=0): #on vérifie que le bob ne s'échappe pas de la grille 
                        if((not self.caseVisitee((x,yBefore))) or i >= 5): #on verifie que la case n'est pas dans la memoire du bob
                            self.coordinates = (x,yBefore)
                            boucle = False
                elif a == 2:
                    if b == 1 :
                        y = yBefore + 1
                    elif b == 2 :
                        y = yBefore - 1
                    if (y<=M-1 and y>=0):
                        if((not self.caseVisitee((xBefore,y))) or i >= 5):
                            self.coordinates = (xBefore,y)
                            boucle = False
    
    #met le bob dans sa nouvelle case
    def deplacerBobCoordonnee(self):
        if(self.coordinates not in grille):
            self.case = Case(self.coordinates) #on créer une case
            self.case.ajouterBob(self) #on ajoute un bob a cette case
            grille[self.coordinates] = self.case #on ajoute la nouvelle case a notre grille
        else :
            self.case = grille[self.coordinates]
            grille[self.coordinates].ajouterBob(self) #on ajoute un bob a la liste de bob de la case de clé coord
        
    def perdreEnergieDeplacement(self):
        eVitesse = 1
        if(speedON):
            eVitesse = (self.speed)**2
        eMasse = 1
        if(massON):
            eMass = self.mass
        ePerception = 0
        if(perceptionON):
            ePerception = 1/5*trunc(self.perception)
        eMemoire = 0
        if(memoryON):
            eMemoire = 1/5*trunc(self.memory)
        
        energyLoss = max((eVitesse * eMasse + ePerception + eMemoire),0.5)
        if(deseaseON and self.sick):
            energyLoss *= 2
        self.energy -= energyLoss
    
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
    def coordAdjacentes(self, coordonnee, perception =-1): #renvoie les case visibles depuis
        if(perception == -1):
            perception = self.perception
        x = coordonnee[0]
        y = coordonnee[1]
        coordonneeAdjacentes = [] #liste de tuples
        for i in range(0,trunc(perception+2)):
            for j in range(0, trunc(perception-i+1)):
                if(i==0):
                    coordonneeAdjacentes.append((x,y+j))
                    coordonneeAdjacentes.append((x,y-j))
                elif(j==0):
                    coordonneeAdjacentes.append((x+i,y))
                    coordonneeAdjacentes.append((x-i,y))
                else:
                    coordonneeAdjacentes.append((x+i,y+j))
                    coordonneeAdjacentes.append((x+i,y-j))
                    coordonneeAdjacentes.append((x-i,y+j))
                    coordonneeAdjacentes.append((x-i,y-j))
                
        #On enleve les coordonnée qui sortent de la grille
        k = len(coordonneeAdjacentes)
        while(k>0):
            k-=1
            coord = coordonneeAdjacentes[k]
            if (coord[0] < 0)or(coord[0]>= N)or(coord[1]<0)or(coord[1]>=M):
                del(coordonneeAdjacentes[k])                
          
        return coordonneeAdjacentes
    
    def nourritureEnVue(self, coordonnee): #renvoie la liste des nourriture 
        #mise à jour de la liste de nourriture
        nourritureEnVue = [] #on vide la liste de tuple
        
        for coord in self.coordAdjacentes(coordonnee) :
            if (coord in grille):
                if (grille[coord].qtite_nourriture != 0):
                    nourritureEnVue.append(coord)
        return nourritureEnVue
    
    #renvoie la distance entre un bob et des coordonnées
    def distance(self, coord):#pourrait très bien ne pas être dans le classe bob
        return abs(coord[0] - self.coordinates[0]) + abs(coord[1] - self.coordinates[1])
    
    #definie la nourriture préférée du bob
    def setNourriturePrefereeDistance(self): #ajouter les bobs
        if(len(self.seenFoods)):
            foods = self.seenFoods
        elif(memoryON and len(self.rememberedFoods)):
            foods = list(self.rememberedFoods.keys())
        else:
            print("Erreur, pas de nourriture en vue ni en mémoire") #on utilise pas setNourriturePreferee si y'a pas de nourriture en vue
            return -1
        
        min = self.distance(foods[0])
        coordPref = foods[0]
        for i in range(1,len(foods)):
            coordN = foods[i]
            if (self.distance(coordN)< min):
                min = self.distance(coordN)
                coordPref = coordN
            elif (len(self.seenFoods) and (self.distance(coordN) == min) and (grille[coordN].qtite_nourriture > grille[coordPref].qtite_nourriture)):
                coordPref = coordN
            elif(not len(self.seenFoods) and (self.distance(coordN) == min) and (self.rememberedFoods[coordN] > self.rememberedFoods[coordPref])):
                coordPref = coordN
        self.coordFavouriteFood = coordPref  
        
    #definie la nourriture préférée du bob
    def setNourriturePrefereeQuantite(self): #ajouter les bobs
        if(len(self.seenFoods)):
            foods = self.seenFoods
        elif(memoryON and len(self.rememberedFoods)):
            foods = list(self.rememberedFoods.keys())
        else:
            print("Erreur, pas de nourriture en vue ni en mémoire") #on utilise pas setNourriturePreferee si y'a pas de nourriture en vue
            return -1
        
        coordPref = foods[0]
        maxNourriture = 0
        for i in range(1,len(foods)):
            coordN = foods[i]
            if(len(self.seenFoods)):
                if (grille[coordN].qtite_nourriture > maxNourriture): #Si on voit des nourritures
                    coordPref = coordN
                elif (grille[coordN].qtite_nourriture == maxNourriture and self.distance(coordN) < self.distance(coordPref)):
                    coordPref = coordN
            else:
                if (self.rememberedFoods[coordN] > maxNourriture): #Si on voit des nourritures
                    coordPref = coordN
                elif ((self.rememberedFoods[coordN] == maxNourriture) and (self.distance(coordN) < self.distance(coordPref))):
                    coordPref = coordN
        self.coordFavouriteFood = coordPref       

    #se deplace de manière optimisée mais aléatoire vers les coordonnées données
    def beeline(self,coordCible): #déplacement en zigzag vers une cible
        #fuire est un "flag" qui dit si on doit fuire ou ses rapprocher des coordonnée 
        if(self.coordinates == coordCible):
            #print("Erreur, le bob est déjà sur cette case")
            return -1
        self.case.enleverBob(self)
        x = coordCible[0] - self.coordinates[0] 
        y = coordCible[1] - self.coordinates[1]
        
        uneCase = 1
        nbCase = self.calculNbCasesDeplacement()*uneCase
        
        self.perdreEnergieDeplacement()
        
        if(nbCase >= self.distance(coordCible)):
            self.coordinates = coordCible
        #probleme pour la fuite c ps bon je peux sortir de la map
        else :
            if(x == 0):
                if(y>0):
                    self.coordinates = (self.coordinates[0],self.coordinates[1]+nbCase)
                else:
                    self.coordinates = (self.coordinates[0],self.coordinates[1]-nbCase)
    
            elif(y == 0):
                if(x>0):
                    self.coordinates = (self.coordinates[0]+nbCase,self.coordinates[1])
                else:
                    self.coordinates = (self.coordinates[0]-nbCase,self.coordinates[1])
            
            else:
                for i in range(nbCase):
                    choix = randint(0,1)
                    if (choix):
                        if(x>0):
                            self.coordinates = (self.coordinates[0]+uneCase,self.coordinates[1])
                        else:
                            self.coordinates = (self.coordinates[0]-uneCase,self.coordinates[1])
                    else:
                        if(y>0):
                            self.coordinates = (self.coordinates[0],self.coordinates[1]+uneCase)
                        else:
                            self.coordinates = (self.coordinates[0],self.coordinates[1]-uneCase)
        self.deplacerBobCoordonnee()  
        return 0      
   
    def chercherNouriture(self): #renvoie 1 si le bob se deplace pour chercher une nourriture 0 s'il ne trouve pas de bouffe
        if(perceptionON):
            self.seenFoods = self.nourritureEnVue(self.coordinates)
            if(len(self.seenFoods) or len(self.rememberedFoods)):
                if(nourriturePref_quantite):
                    self.setNourriturePrefereeQuantite()
                else:
                    self.setNourriturePrefereeDistance()
                self.beeline(self.coordFavouriteFood)
                self.previousAction = CHERCHER_NOURRITURE
                return True
            elif(self.coordClosestPrey):
                self.beeline(self.coordClosestPrey)
                self.previousAction = CHASSER
                return True
            else:
                return False
        else:
            return False    
    
    def bobsEnVue(self):
        bobsEnVue = []
        coordAdj = self.coordAdjacentes(self.coordinates)
        #coordAdj.remove(self.coordinates)
        for coord in coordAdj:
            if (coord in grille) and (len(grille[coord].bobs)!=0) :
                bobsEnVue.append(coord)
        return bobsEnVue
        
    #calcul le predateur le plus proche mais aussi la proie la plus proche
    #peut être que c'est mieux de séparer en deux fonction jsp        
    def enDanger(self):
        #bobsEnVue = self.bobsEnVue()
        bobEnDanger = False
        coordPredateurLePlusProche = ()
        coordProieLaPlusProche = ()
        min_distance_predateur = trunc(self.perception)
        min_distance_proie = trunc(self.perception)
        for coord in self.bobsEnVue():
            for otherBob in grille[coord].bobs:
                if(not (otherBob is self) and (not tribesON or self.tribe != otherBob.tribe)):
                    distance = self.distance(otherBob.coordinates)
                    if (otherBob.mass > 3/2*self.mass):
                        bobEnDanger = True
                        if(distance <= min_distance_predateur):
                            min_distance_predateur = distance
                            coordPredateurLePlusProche = otherBob.coordinates  
                    elif(otherBob.mass < 2/3*self.mass):
                        distance = self.distance(otherBob.coordinates)
                        if(distance <= min_distance_proie):
                            min_distance_proie = distance
                            coordProieLaPlusProche = otherBob.coordinates  
        self.coordClosestPredator = coordPredateurLePlusProche   
        self.coordClosestPrey = coordProieLaPlusProche
        return bobEnDanger
            
    def fuire(self,coordCible): #déplacement en zigzag pour fuir une cible        
        x = coordCible[0] - self.coordinates[0] 
        y = coordCible[1] - self.coordinates[1]
                
        nbCase = self.calculNbCasesDeplacement()
        
        if(nbCase):
            self.perdreEnergieDeplacement()
            self.case.enleverBob(self)

            for i in range(nbCase):
                deplacementFait = False     
                    
                if(not deplacementFait): #on s'eloigne de la cible
                    choix = randint(0,1)
                    deplacementFait = True
                    if (choix):
                        if(x>0 and self.coordinates[0]-1>=0):
                            self.coordinates = (self.coordinates[0]-1,self.coordinates[1])
                        elif(self.coordinates[0]+1<N-1):
                            self.coordinates = (self.coordinates[0]+1,self.coordinates[1])
                        else:
                            deplacementFait = False
                    else:
                        if(y>0 and self.coordinates[1]-1>=0):
                            self.coordinates = (self.coordinates[0],self.coordinates[1]-1)
                        elif(self.coordinates[0]+1<N-1):
                            self.coordinates = (self.coordinates[0],self.coordinates[1]+1)
                        else:
                            deplacementFait = False
            self.deplacerBobCoordonnee() 
        else:
            deplacementFait = True #Si le bob à une vitesse trop faible et donc ne peux pas bouger

        if(deplacementFait): #si le bob n'a pas pu s'eloigner on renvoie false
            self.previousAction = FUIRE
            return True
        else:
            return False      

#memoire
    
    def nourritureAMemoriser(self):
        ancienneNourriture = self.nourritureEnVue(self.previousCoordinates) 
        nourritureEnVue = self.nourritureEnVue(self.coordinates)
        nouvelleNourriture = list(set(ancienneNourriture) 
                                  - set(nourritureEnVue)) #nourriture en vue - ancienne nourriture
        return nouvelleNourriture
    
    def nourritureAOublier(self):
        nourritureOubliee = []
        for n in self.rememberedFoods:
            if(self.distance(n)<=trunc(self.perception)):
                nourritureOubliee.append(n)
        return nourritureOubliee
    
    def setNourritureMemorisee(self):
        #on met a jour la liste de nourriture mémorisées
        for coord in self.nourritureAOublier():
            self.rememberedFoods.pop(coord)
        for coord in self.nourritureAMemoriser():
            self.rememberedFoods[coord]=grille[coord].qtite_nourriture
        
        self.availableMemory = trunc(self.memory) - len(self.rememberedFoods)
        
        #on supprime des nourriture si y'en à trop en memoire
        while(self.availableMemory<0): #on oublie des nourritures tant qu'on en à plus en memoire que la mémoire totale
            max = 0
            for c in self.rememberedFoods: #on calcule quelle est la nourriture la plus loin du bob à oublier en priorité
                if (self.distance(c) > max):
                    max = self.distance(c)
                    coord = c
            #self.rememberedFoods.pop(coord)
            self.availableMemory += 1
        
    def setCaseMemorisee(self):
        self.rememberedSquares.append(self.coordinates)
        while(len(self.rememberedSquares) > (2 * trunc(self.availableMemory))):
            self.rememberedSquares.pop(0)
 
#reproduction sexuée 
    def partenaireDisponible(self): #renvoie un bob pret à faire un bébé 
        for b in self.case.bobs:
            if((b.energy >= 150) and (not b.enDanger()) and (b != self)): #fonction enDanger à remplacer par la fonction de Huy correspondante
                if(not tribesON or b.tribe == self.tribe):
                    return b
        return None

#Attaquez vos semblables s'ils manquent de nourriture    
    def cannibal(self):
        if not self.chercherNouriture():
            if self.enDanger() and self.coordClosestPrey:
                self.fuire(self.coordClosestPrey)
                return True
            elif self.coordClosestPrey:
                bob_predateur = grille[self.coordClosestPrey].bobs[0]
                self.attack(bob_predateur)
                return True
        return False
        
#fonction de communication
    #le bob printf ses coordonnee et son energie
    def speak(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordinates, "J'ai",self.energy,"energie")
    
    #le bob printf ses coordonnee, sa vitesse et son energie
    def speakSpeed(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordinates,"J'ai une vitesse de ",self.speed, "J'ai",self.energy,"energie")

    #le bob print coord, vitesse, preception
    def speakPerception(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordinates,"J'ai une vitesse de ",self.speed, "J'ai une preception de ",self.perception, "J'ai",self.energy,"energie")
        
    def speakMass(self): #juste pour faire des tests
        print("(Bob) Je suis en : ",self.coordinates,"J'ai une masse de ",self.mass)
    
    def speakPreviousAction(self):
        print("(Bob) Je suis en : ",self.coordinates,"J'ai",trunc(self.energy),"energie","Ma dernière action était : ",self.previousAction)

    
    
