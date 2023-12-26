#La grille
grille={}

#Les listes de Bobs
allBobs = []
aliveBobs = []
deadBobs = []


#Paramètres simulation :
N = 2 #100 Length or width of the map (grid of N*N)
numberBob = 100 #100 Number of Bobs at the begining 
numberFood = 200 #200 Number of food points par day


T = 50 #100 Number of ticks in a day

bobMaxE = 200 #200 Max of energy of a bob
bobSpawnE = 100 #100 Quantity of energy when spawning
bobBirthE = 50 #50 Quantity of enery for babies
bobLaborE = 150 #150 Quantity of energy lost when giving birth

foodE = 100 #100 Quantity of energy per food point

bobS = 1 #1 Speed before mutation
bobM = 1 #1 Mass before mutation
bobP = 1 #1 Perception before mutation
bobMem = 0 #0 Memory before mutation

#Paramètre affichage graphique :
SCREEN_WIDTH=1280/2
SCREEN_HEIGHT=720/2