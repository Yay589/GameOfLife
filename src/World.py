from collections import defaultdict
import pygame
import random


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

    def convert_position(self, position):
        return [150 + position[0] * 10 - position[1] * 10, 100 + position[0] * 5 + position[1] * 5]

    def addOnMap(self, _Object):
        # {'(x,y)': sprite_Object , ...}
        key = str(random.choice(self.list_x_y))
        if key in self.world.keys():
            print("There is a collision between two sprites")
        self.world[key].append(_Object)

    def aviableNearbyPosition(self, newPosition):  # refaire le calcule de l
        l = [[(newPosition[0]-dup1), (newPosition[1]-dup2)]
             for dup1 in (-1, 1) for dup2 in (-1, 1)]
        res = []
        for i in l:
            for j in self.list_x_y:
                if i == j:
                    res.append(i)
        return random.choice(res)

    # met a jour la nouvel position et la mofifie si celle donée est invalide //à finir.
    def update(self, _Object, newPosition):
        if _Object not in self.world.values():
            self.addOnMap(_Object)
        tempDict = defaultdict(list)
        Position = self.convert_position(newPosition)
        if Position not in self.list_x_y:
            # reprendre à partir ce cette ligne
            Position = self.aviableNearbyPosition(newPosition)
        for key, value in self.world.items():
            if key == str(_Object.rect.center):
                tempDict[str(newPosition)].remove(_Object.rect.center)
                tempDict[str(newPosition)].append([150 + newPosition[0] * 10 -
                                                   newPosition[1] * 10, 100 + newPosition[0] * 5 + newPosition[1] * 5])


pygame.init()

# Création d'une fenêtre
screen = pygame.display.set_mode((800, 600))

# Création d'une instance de la classe World
world_instance = World(3, 4)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Efface l'écran
    screen.fill((255, 255, 255))

    # Dessine l'image à partir de world_instance
    for i in world_instance.list_x_y:
        screen.blit(world_instance.image, i)

    # Actualise l'écran
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()
