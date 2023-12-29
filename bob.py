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

__authors__ = ("Célestine")
__date__ = "2030-12-10" #10 decembre
__version__= "1.0" 

from random import *
from parametre import *
from case import Case
from math import trunc


class Bob():
    def __init__(self, 
                 skiping = False, #True si le bob naît d'un autre bob
                 bobEnergy = bobSpawnE, 
                 bobSpeed = bobS, 
                 bobMass = bobM, 
                 bobPerception = bobP, 
                 bobMemory = bobMem,
                 coord = (randint(0,N-1),randint(0,N-1)) ) :
        #coordonnee
        self.coordinates = coord #avec randint les deux bornes sont inclusives
        self.previousCoordinates = coord #pour l'instant on va dire ça s'il vient de pop
        
        #ajout du bob dans la grille
        if(coord not in grille):
            self.case = Case(coord)
            self.case.ajouterBob(self)
        else :
            self.case = grille[coord]
            self.case.ajouterBob(self) #on ajoute un bob a la liste de bob de la case de clé coord
        
        #booleans
        self.skipingTurn = skiping #indique si le bob doit sauter ce tour (jour de naissance ou s'il a fait un bebe)
        self.dead = 0

        #caracteritiques fixes du bob
        self.energy = bobEnergy
        self.speed = bobSpeed
        self.mass = bobMass
        self.perception = bobPerception
        self.memory = bobMemory
        
        #vitesse
        self.speedBuffer = 0
        
        #perecption
        self.seenFoods = []
        self.coordFavouriteFood = None
        
        #memoire
        self.availableMemory = bobMemory #pour l'instant aucune case mémoirisé donc memoire dispo = memoire totale
        self.rememberedFoods = []
        self.rememberedSquares = []

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
            self.previousCoordinates = self.coordinates #met a jour coordonnee precedente
            #calcul des données héreditaire
            vitesseBebe = self.speed + random()%0.2 - 0.1
            perceptionBebe = max((self.perception + randint(-1,1)),0)
            memoireBebe = self.memory + randint(-1,1)
            #creation du bebe
            allBobs.append(Bob(birthDay = 1, bobEnergy = bobBirthE, bobSpeed = vitesseBebe, bobPerception = perceptionBebe, bobMemory = memoireBebe, coord = self.coordinates))
            #perte d'energie
            self.energy -= bobLaborE
            return 1
        else:
            return 0
       
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
                    if (y<=N-1 and y>=0):
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
        #On a pas besoin de tester si le bob à la droit de jouer dans chaque fonction prck on le fait une fois au debut avec la fonction deja joué
        # if(self.skipingTurn):
        #     self.skipingTurn = False
        #     #print("This bob just apeared, wait till the next tic")
        #     return -1

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
      
    #permet de deplacer un bob, soit pour chercher de la nourriture, soit aléatoirement  
    def bobDeplacement(self):
        self.previousCoordinates = self.coordinates
        if(not self.chercherNouriture()):
            self.bouger()
        self.setNourritureMemorisee()
        self.setCaseMemorisee()
    
#perception
    def coordAdjacentes(self, coordonnee, perception): #renvoie les case visibles depuis
        x = coordonnee[0]
        y = coordonnee[1]
        coordonneeAdjacentes = [(coordonnee)] #liste de tuples
        for i in range(0,int(perception+2)):
            for j in range(0, int(perception-i+1)):
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
    
    def nourritureEnVue(self, coordonnee, perception): #renvoie la liste des nourriture 
        #mise à jour de la liste de nourriture
        nourritureEnVue = [] #on vide la liste de tuple
        
        for coord in self.coordAdjacentes(coordonnee,perception) :
            if (coord in grille):
                if (grille[coord].qtite_nourriture != 0):
                    nourritureEnVue.append(coord)
        return nourritureEnVue

        #anciennes version des deux fonctions :
    #renvoie une liste qui contient les tuples des coordonnée adjactente à la case du bob
    # def coordAdjacentes(self):
    #     x = self.coordinates[0]
    #     y = self.coordinates[1]
    #     coordonneeAdjacentes = [(self.coordinates)] #liste de tuples
    #     for i in range(0,self.perception+2):
    #         for j in range(0,self.perception-i+1):
    #         #peut être ajouter une verification que ca peut bien être dans la grille en terme de coordonnee
    #             if(i==0):
    #                 coordonneeAdjacentes.append((x,y+j))
    #                 coordonneeAdjacentes.append((x,y-j))
    #             elif(j==0):
    #                 coordonneeAdjacentes.append((x+i,y))
    #                 coordonneeAdjacentes.append((x-i,y))
    #             else :
    #                 coordonneeAdjacentes.append((x+i,y+j))
    #                 coordonneeAdjacentes.append((x+i,y-j))
    #                 coordonneeAdjacentes.append((x-i,y+j))
    #                 coordonneeAdjacentes.append((x-i,y-j))
    #     return coordonneeAdjacentes
 
    #met a jour la liste de nourriture en vue du bob, renvoie le nombre de nourritures vues
    #peut être mieux de juste renoyer la liste comme ça les bobs aurait pas besoin de s'en souvenir
    # def nourritureEnVue(self): #renvoie le nombre de nourriture
    #     x = self.coordinates[0]
    #     y = self.coordinates[1]
        
    #     #mise à jour de la liste de nourriture
    #     self.nourritureEnVue = [] #on vide la liste de tuple
        
    #     for coord in self.coordAdjacentes() :
    #         if (coord in grille):
    #             if (grille[coord].qtite_nourriture != 0):
    #                 print("Le bob voit une nourriture")
    #                 self.nourritureEnVue.append(coord)
    #     return len(self.nourritureEnVue)
    
    #renvoie la distance entre un bob et des coordonnées
    def distance(self, coord):#pourrait très bien ne pas être dans le classe bob
        return abs(coord[0] - self.coordinates[0]) + abs(coord[1] - self.coordinates[1])
    
    #definie la nourriture préférée du bob
    def setNourriturePreferee(self):
        if(len(self.seenFoods)==0):
            print("Erreur, pas de nourriture en vue") #on utilise pas setNourriturePreferee si y'a pas de nourriture en vue
            return -1
        min = self.distance(self.seenFoods[0])
        coordPref = self.seenFoods[0]
        for i in range(1,len(self.seenFoods)):
            coordN = self.seenFoods[i]
            if (self.distance(coordN)< min):
                coordPref = coordN
            elif ((self.distance(coordN) == min) and (grille[coordN].qtite_nourriture > grille[coordPref].qtite_nourriture)):
                coordPref = coordN
        self.coordFavouriteFood = coordPref       

    #se deplace de manière optimiser mais aléatoire vers les coordonnées données
    def beeline(self,coordCible): #déplacement en zigzag vers une cible
        if(self.coordinates == coordCible):
            print("Erreur, le bob est déjà sur cette case")
            return -1
        self.case.enleverBob(self)
        x = coordCible[0] - self.coordinates[0] 
        y = coordCible[1] - self.coordinates[1]
        nbCase = self.calculNbCasesDeplacement()
        
        self.perdreEnergieDeplacement()
        
        if(nbCase >= self.distance(coordCible)):
            self.coordinates = coordCible
        
        else :
            for i in range(nbCase):
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
                    choix = randint(0,1)
                    if (choix):
                        if(x>0):
                            self.coordinates = (self.coordinates[0]+1,self.coordinates[1])
                        else:
                            self.coordinates = (self.coordinates[0]-1,self.coordinates[1])
                    else:
                        if(y>0):
                            self.coordinates = (self.coordinates[0],self.coordinates[1]+1)
                        else:
                            self.coordinates = (self.coordinates[0]-1,self.coordinates[1]-1)
        self.deplacerBobCoordonnee()  
        return 0      
   
    def chercherNouriture(self): #renvoie 1 si le bob se deplace pour chercher une nourriture 0 s'il ne trouve pas de bouffe
        setTempNourriture = set(self.nourritureEnVue(self.coordinates, self.perception))
        setTempNourriture |= set(self.rememberedFoods) #ajout avec la memoire
        nourriture = list(setTempNourriture)
        self.seenFoods = nourriture
        if(len(nourriture)):
            self.setNourriturePreferee()
            self.beeline(self.coordFavouriteFood)
            return 1
        else:
            return 0

#memoire
    
    def nourritureAMemoriser(self):
        ancienneNourriture = self.nourritureEnVue(self.previousCoordinates, self.perception) 
        nourritureEnVue = self.nourritureEnVue(self.coordinates,self.perception)
        nouvelleNourriture = list(set(ancienneNourriture) 
                                  - set(nourritureEnVue)) #nourriture en vue - ancienne nourriture
        return nouvelleNourriture

    #jsp pk cette version là elle marche pas
    # def nourritureAOublier(self):
    #     #nourritureMemorise - cases adjactente 
    #     nourritureOubliee = list(set(self.rememberedFoods) 
    #                              - set(self.coordAdjacentes(self.coordinates,self.perception)))
    #     print("Cases adj : ",nourritureOubliee)
    #     self.speak()
    #     return nourritureOubliee
    
    def nourritureAOublier(self):
        nourritureOubliee = []
        for n in self.rememberedFoods:
            if(self.distance(n)<=self.perception):
                nourritureOubliee.append(n)
        return nourritureOubliee
    
    def setNourritureMemorisee(self):
        tempSet = set(self.rememberedFoods)
        tempSet |= set(self.nourritureAMemoriser())
        self.rememberedFoods = list(tempSet - set(self.nourritureAOublier()))
        
        self.availableMemory = self.memory - len(self.rememberedFoods)
        while(self.availableMemory<0):
            self.rememberedFoods.pop(0) #pour l'instant on en enleve un au hasard, a modifier evetuellement pour supprime la plus loin
            self.availableMemory += 1
        # if(len(self.rememberedFoods)==0):
        #     print("Pas de nourriture mémorisée")
        # else:
        #     print("Nourritures mémorisées : ",self.rememberedFoods)
    
    def setCaseMemorisee(self):
        self.rememberedSquares.append(self.coordinates)
        while(len(self.rememberedSquares) > (2 * self.availableMemory )):
            self.rememberedSquares.pop(0)
 
#reproduction sexuée 
    def reproductionSexuee(self): #renvoie 1 si le bob fait un bebe et 0 sinon
        if(self.energy < 150): #remplacer 150 par une variable 
            #print("Pas assez d'energie")
            return 0 #pas assez d'energie
        bob = self.partenaireDisponible() #avec x un fonction qui renvoie un bob qui à assez d'energie
        if(bob==None):
            #print("Pas de partenaire disponible")
            return 0 #pas de partenaire dispnnible
        
        #calcul des caractéritiques du bébé :
        vitesseBebe = max(((self.speed + bob.speed)/2 + random()%0.2 - 0.1),0)
        perceptionBebe = max(((self.perception + bob.perception)/2 + randint(-1,1)),0)
        memoireBebe = max(((self.memory + bob.memory)/2 + randint(-1,1)),0)
        #creation du bebe
        allBobs.append(Bob(skiping = True, bobEnergy = bobSexBirthE, bobSpeed = vitesseBebe, bobPerception = perceptionBebe, bobMemory = memoireBebe, coord = self.coordinates))
        #perte d'energie
        self.energy -= bobSexLaborE
        bob.energy -= bobSexLaborE
        bob.tourJoue = True
        return 1
    
    def partenaireDisponible(self): #renvoie un bob pret à faire un bébé 
        for b in self.case.bobs:
            b.speak()
            if((b.energy >= 150) and (not b.enDanger()) and (b != self)): #fonction enDanger à remplacer par la fonction de Huy correspondante
                return b
        return None
    
    def dejaJoue(self):
        if(self.skipingTurn):
            self.skipingTurn = False
            return True
        else:
            return False

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
        if(self.dead == 1):
            return -1

        if(self.case.qtite_nourriture != 0):
            self.previousCoordinates = self.coordinates #mise a jour des coord precedentes
            #calcul du gain d'energie et energie restante sur la case
            faim = bobMaxE - self.energy
            reste = self.case.qtite_nourriture - faim
            if (reste <= 0) :
                self.energy += self.case.qtite_nourriture
                self.case.qtite_nourriture = 0
            else :
                self.case.qtite_nourriture -= faim  #on enleve à la nourriture l'énergie que le bob consomme
                self.energy = bobMaxE
            return 1
        else :
            return 0

    #indique si deux bobs partagent une même case, pas sure que cette fonction soit utile.
    def memeCase(self, b):
        if(self.coordinates == b.coordonnee): return 1
        else : return 0
    
    #indique si un bob est seul sur sa case
    def seul(self):
            #version si les bobs stockent leur case
        #return len(self.case.bobs)==1 #si la taille de la liste de bob de sa case est 1 il est seul
            #version si on dit que les bobs ne sockent plus leur case :
        return len(grille[self.coordinates].bobs) == 1
    
    #choisi un bob parmis ceux qui sont sur la même case
    #cette fonction est inutile vu qu'on va remelanger le dict plutôt
    def choisirUnBob(self): #peut être mieux de mettre ça dans case.py jsp
        n = len(grille[self.coordinates].bobs)
        indexBobChoisi = randint(0,n-1)
        return indexBobChoisi
    
#les deux fonctions suivante enfaite c'est Huy qui fait ça
    def enDanger(self):
        #si le bob voit un prédateur la fonction renvoie un
        return 0
    #renvoie 1 si le bob à besoin de se proteger (et fait le nécessaire) et 0 si le bob n'est pas en danger
    def seProteger(self):
        if(self.enDanger):
            #le bob fait une action pour se proteger
            return 1
        else : return 0
    
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
