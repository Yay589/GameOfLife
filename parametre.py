from collections import defaultdict

Relancer = True
###########################################################
#Variables qui peuvent être modifiées EN DÉBUT DE PARTIE :
#Paramètres simulation :
N = 100
M = 100
numberBob = 100

###########################################################
#Variable qui peuvent être modifiées EN COURS DE PARTIE :
    #Paramètre ON/OFF :
graphicalInterfaceON = True
#True : ON 
#False : OFF
soloReproductionON = True
duoReproductionON = True
speedON = True
massON = True
perceptionON = True
memoryON = True

    #Valeurs des variables :
numberFood = 60 #200 Number of food points par day
foodE = 50 #100 Quantity of energy per food point

T = 50 #100 Number of ticks in a day

bobMaxE = 200 #200 Max of energy of a bob
bobSpawnE = 100 #100 Quantity of energy when spawning
bobBirthE = 50 #50 Quantity of energy for babies
bobLaborE = 150 #150 Quantity of energy lost when giving birth
bobMinSexE = 150 #150 Minimal quanity of energy requiered for sexual reproduction
bobSexBirthE = 100 #100 Quantity of energy for babies with sexual reproduction
bobSexLaborE = 100 #100 Quantity of energy lost when giving birth with sexual reproduction

#caracteristiques -> pas modifiable mais si c'est plus bas ça fait un bug :
ENERGIE = 1
VITESSE = 2
MASSE = 3
PERCEPTION = 4
MEMOIRE = 5
#modifiable :
chosenCarateristic = MASSE # Indique quelle caractéristique doit être representée par la couleur des bobs
#ENERGIE - VITESSE - MASSE - PERCEPTION - MEMOIRE

    #modes spéciaux
#Aléatoire start : Pour pouvoir commencer avec des caractéritiques aléatoire
#Pour l'instant ça va fonctionner que si toutes les caractéritique sont activées : 
randomStartOn = True
maxRandomSpeed = 3
maxRandomMass = 3
maxRandomPerception = 6
maxRandomMemory = 4
#Gentillesse
kindnessON = True
birthKindness = 20 #Point de gentillesse à la naissance (pas génétique)
kidnessAdded = 5 #Point de gentillesse gagnés quand on recoit de la nourriture
#Maladie
deseaseON = True
chancesOfFoodPoisoning = 50 #1000, 1 chance sur 1000 de tomber malade
nbSickTics = 20 #nombre de jour où le bob reste malade
#Tribues
tribesON = True
tribesRandom = True
#Education
educationON = True
chancesOfBeingBornEducated = 5 #10, 1 chance out of 10


#Est ce que les bobs prefere les nourriture proches ou grosses
nourriturePref_quantite = True
#True Indique si la nourriture doit être favorisée 
#par les bobs en fonction de la quantité (True) ou de la distance (False)
#Fonctionnement normal -> quantité



###########################################################
#Variable qui ne doivent pas être modifiées par les joueurs :

#La grille     
grille = {}

#caratéristiques de base
bobS = 1 #1 Speed before mutation
bobM = 1 #1 Mass before mutation
bobP = 1 #1 Perception before mutation
bobMem = 0 #0 Memory before mutation

#Les listes de Bobs
allBobs = []
deadBobs = []

#previous action
NAITRE = 0
MANGER = 1
REPRODUCTION_SOLO = 2
REPRODUCTION_DUO = 3
FUIRE = 4
CHASSER = 5
CHERCHER_NOURRITURE = 6
DEPLACEMENT_ALEATOIRE = 7
MOURIR_ENERGIE = 8
MOURIR_ATTAQUE = 9

#Nom des tribues : 
FEU = 1
GLACE = 2
TERRE = 3
EAU = 4

#Paramètre affichage graphique :
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

#list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(N)]