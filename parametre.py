from collections import defaultdict

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
        self.supprimer() #a enlever si on enlevela liste de bob et qu'on a un dictionnaire temporaire plutôt
    
    def ajouterNourriture(self, qtite_nourriture = 100):
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

<<<<<<< HEAD

###########################################################
#Variables qui peuvent être modifiées EN DÉBUT DE PARTIE :
#Paramètres simulation :
N = 20 #100 Length or width of the map (grid of N*N)
numberBob = N*2 #100 Number of Bobs at the begining 
=======
###########################################################
#Variables qui peuvent être modifiées EN DÉBUT DE PARTIE :
#Paramètres simulation :
N = 30 #100 Length or width of the map (grid of N*N)
numberBob = 50 #100 Number of Bobs at the begining 
>>>>>>> 66c21dc0168070e014e39b1b83088cd145a18e03

bobS = 1 #1 Speed before mutation
bobM = 1 #1 Mass before mutation
bobP = 1 #1 Perception before mutation
bobMem = 0 #0 Memory before mutation

###########################################################
#Variable qui peuvent être modifiées EN COURS DE PARTIE :
    #Paramètre ON/OFF :
graphicalInterfaceON = True #False : terminal, True : graphique
#True : ON 
#False : OFF
soloReproductionON = True
duoReproductionON = True
speedON = True
massON = True
perceptionON = True
memoryON = True

    #Valeurs des variables :
<<<<<<< HEAD
numberFood = 20 #200 Number of food points par day
=======
numberFood = 100 #200 Number of food points par day
>>>>>>> 66c21dc0168070e014e39b1b83088cd145a18e03
foodE = 50 #100 Quantity of energy per food point

T = 100 #100 Number of ticks in a day

bobMaxE = 200 #200 Max of energy of a bob
bobSpawnE = 100 #100 Quantity of energy when spawning
bobBirthE = 50 #50 Quantity of energy for babies
bobLaborE = 150 #150 Quantity of energy lost when giving birth
bobMinSexE = 150 #150 Minimal quanity of energy requiered for sexual reproduction
bobSexBirthE = 100 #100 Quantity of energy for babies with sexual reproduction
bobSexLaborE = 100 #100 Quantity of energy lost when giving birth with sexual reproduction

bobS = 1 #1 Speed before mutation
bobM = 1 #1 Mass before mutation
bobP = 1 #1 Perception before mutation
bobMem = 0 #0 Memory before mutation

#Paramètre affichage graphique :
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(N)]
>>>>>>> 66c21dc0168070e014e39b1b83088cd145a18e03

