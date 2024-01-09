import pygame
import random


class Nourriture(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('data/images/apple.png'))
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


class BOB(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('data/images/0.png'))
        self.sprites.append(pygame.image.load('data/images/1.png'))
        self.sprites.append(pygame.image.load('data/images/2.png'))
        self.sprites.append(pygame.image.load('data/images/3.png'))
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.energy = 100

    def update(self):

        self.current_sprite += 1
        self.energy -= 5

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        # assigning the next image of the animation
        self.image = self.sprites[self.current_sprite]

    def bouger(self, grid_cell_size, listPoints, cx, cy):
        # Déplacement aléatoire en multiples de la taille de la cellule
        dx = random.randint(-1, 1) * grid_cell_size
        # Déplacement aléatoire en multiples de la taille de la cellule
        dy = random.randint(-1, 1) * grid_cell_size

        selection = [(self.rect.center[0]+cx + dx_, self.rect.center[1]+cy + dy_) for dx_ in [-dx, 0, dx]
                     for dy_ in [-dy, 0, dy]]
        posibilities = []
        for i in selection:
            if i in listPoints:
                posibilities.append(i)
        # print("selection = ", selection)
        # print("posibilities = ", posibilities)
        # print("listPoints = ", listPoints)
        point = random.choice(posibilities)
        new_x, new_y = point

        self.rect.x = new_x-cx
        self.rect.y = new_y-cy
