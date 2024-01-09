from collections import defaultdict

import random

# Initialize Pygame




class World:


    def __init__(self, n, m):
        self.world = defaultdict(list)
        self.n = n
        self.m = m
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(self.n) for y in range(self.m)]
        
        

    def addOnMap(self, List_of_object):
        
        # listKeys=[i for i in self.world.keys()]
        
        # if str(position) in listKeys:
        #     print(f"{position} is in {self.world.keys()} so there is a collision")

        # Read positions from the 'save.txt' file
        #with open('src/save.txt', 'r') as file:
        #    positions= file.read().splitlines()

        allocated_positions = set() 

        for obj, position_str in zip(List_of_object, positions):
            position = eval(position_str)
    
            if str(position) in allocated_positions:
                print(f"Position {position} is already allocated. Skipping object.")
            else:
                obj.rect.center = position
                self.world[str(position_str)].append(obj)
                allocated_positions.add(str(position))
                
        
        
    
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

    def save_game(self):
        with open('src/save.txt', 'w') as file:
            for key, value in self.world.items():
                print(key)
                print(value)
                print("\n")
                file.write(f"{key},{value}\n")
            
    






