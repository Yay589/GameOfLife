#La grille
grille={}

#Les listes de Bobs
allBobs = []
aliveBobs = []
deadBobs = []


#Paramètres simulation :
N = 10 #100 Length or width of the map (grid of N*N)
numberBob = 100 #100 Number of Bobs at the begining 
numberFood = 200 #200 Number of food points par day
foodE = 100 #100 Quantity of energy per food point

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
SCREEN_WIDTH=1280/2
SCREEN_HEIGHT=720/2
