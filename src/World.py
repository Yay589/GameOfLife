from collections import defaultdict
import pygame
import random

# Initialize Pygame
pygame.init()

# Define the screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Your Game Title')

class World:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.world = defaultdict(list)
        

    def addOnMap(self, _Object):
        
        listKeys=#[i for i in self.world.keys()]
        position = random.choice(self.list_x_y)
        
        if str(position) in listKeys:
            print(f"{position} is in {self.world.keys()} so there is a collision")
            
        self.world[str(position)].append(_Object)
        #print("self.world.keys() = ",[i for i in self.world.keys()])
        
        _Object.rect.center = list(position)
        
        #print("type (obj.rect.center) = ", type(_Object.rect.center))
        #print("addonmap => ", self.world)

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
            print(_Object, "is not in", listValue)
            print("_Object.rect.center =", _Object.rect.center, "world = ",self.world)
        tempDict = defaultdict(list)
        tempDict = self.world.copy()
        Position = self.availableNearbyPosition(list(_Object.rect.center))
        #print("newPosition = ", Position)
        #print("before changes :  self.world = ", self.world)
        
        #retirer object de son ancienne positiion (=retirer de la key)
        for key, value in self.world.items():
            if key == str(list(_Object.rect.center)) and _Object in [i for i in value]:
                #print("TROUVÉÉÉÉÉÉÉÉÉÉÉÉ   object = ",_Object," and key = ",key)
                #on change cette valeur sur le tompons tempDict
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
        
        #on renouvel maintenant la valeur de self.world
        self.world = tempDict.copy()
        #print("after changes :  self.world = ", self.world)
        
        #print("HEYYY world = ", self.world)

    def draw(self):
        screen.fill((255, 255, 255))
        for i in self.list_x_y:
            screen.blit(self.image, i)
            #grass_image.set_colorkey((0, 0, 0))

        for k, v in self.world.items():
            for obj in v:
                screen.blit(obj.image, list(eval(k)))
                #print("\neval(k) = ", eval(k))
                #print("obj.rect.center = ", obj.rect.center)                
                obj.current_sprite+=1

        pygame.display.flip()

class GameObject(pygame.sprite.Sprite):
    def __init__(self,id):
        super().__init__()
        self.id=id
        self.sprites = []
        self.sprites.append(pygame.image.load('data/images/0.png').convert())
        self.sprites.append(pygame.image.load('data/images/1.png').convert())
        self.sprites.append(pygame.image.load('data/images/2.png').convert())
        self.sprites.append(pygame.image.load('data/images/3.png').convert())
        self.current_sprite = 0
        
        if self.current_sprite > 3:
            self.current_sprite=0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = list([0, 0])

world = World(n=30, m=30)
object1 = GameObject(1)
object2 = GameObject(2)
object3 = GameObject(3)

world.addOnMap(object1)
world.addOnMap(object2)
world.addOnMap(object3)

running = True
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    world.draw()
    
    world.move(object1)
    world.move(object2)
    world.move(object3)
    
    clock.tick(30)
    
pygame.quit()




