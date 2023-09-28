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
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5]
                         for x in range(self.n) for y in range(self.m)]
        self.world = defaultdict(list)
        self.image = pygame.image.load('data/images/grass.png').convert()
        self.image.set_colorkey((0, 0, 0))
        for i in self.list_x_y:
            self.rect = self.image.get_rect()
            self.rect.center = i
            
        # camera
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.camera_borders = {'left': 200,
                               'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size(
        )[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size(
        )[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # parametre
        self.keyboard_speed = 15
        self.mouse_speed = 0.2

        # zoom
        self.zoom_scale = 1
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(
            self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(
            center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(
            self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def convert_position(self, position):
        return [150 + position[0] * 10 - position[1] * 10, 100 + position[0] * 5 + position[1] * 5]

    def addOnMap(self, _Object):
        listKeys=[i for i in self.world.keys()]
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

    def move(self, _Object): #revoir les dict vide au début à linitialisation de la key (peut être tmp=world puis on modifie tmp comme ça on ne retouche pas world)
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





