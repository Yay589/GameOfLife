from collections import defaultdict
import pygame
import random

# Initialize Pygame
pygame.init()



class World:
    def __init__(self, n, m):
        self.world = defaultdict(list)
        self.n = n
        self.m = m
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(self.n) for y in range(self.m)]
        
        

    def addOnMap(self, _Object):
        
        listKeys=[i for i in self.world.keys()]
        position = random.choice(self.list_x_y)
        
        if str(position) in listKeys:
            print(f"{position} is in {self.world.keys()} so there is a collision")
            
        self.world[str(position)].append(_Object)
        
        _Object.rect.center = list(position)
        

    
    def availableNearbyPosition(self, Position):
        l = [[(Position[0] - dup1), (Position[1] - dup2)]
             for dup1 in (-10, 10) for dup2 in (-5, 5)]
        res = []
        for i in l:
            for j in self.list_x_y:
                if i == j:
                    res.append(i)
        return random.choice(res)

    def move(self, _Object):
        
        listValue = [i[j] for i in self.world.values() for j in range(len(i))]+[]
        if _Object.id not in [i.id for i in listValue]:

            self.addOnMap(_Object)
        
        tempDict = defaultdict(list)
        tempDict = self.world.copy()
        Position = self.availableNearbyPosition(list(_Object.rect.center))

        
        #retirer object de son ancienne positiion (=retirer de la key)
        for key, value in self.world.items():
            if key == str(list(_Object.rect.center)) and _Object in [i for i in value]:
                tempDict[str(list(_Object.rect.center))]=[]
                for i in value :
                    if i != _Object:
                        tempDict[key].append(i)
            #si en retirant _Object de son ancien enplacement, il ne reste pas d'autre _Objet, alors supprimer la key. ça évite de remplir le dict avec rien.
            if tempDict[key] ==[]:
                del tempDict[key]
        
        #on ajourte l'objet à la nouvel position et on change ses coordonné dans .rect.center
        tempDict[str(Position)].append(_Object)
        _Object.rect.center = list(Position)
        
        self.world = tempDict.copy()

pygame.quit()




