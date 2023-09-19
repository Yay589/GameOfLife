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

    def bouger(self, grid_width, grid_height, grid_cell_size):
        # Déplacement aléatoire en multiples de la taille de la cellule
        dx = random.randint(-1, 1) * grid_cell_size
        # Déplacement aléatoire en multiples de la taille de la cellule
        dy = random.randint(-1, 1) * grid_cell_size

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Vérifier que la nouvelle position reste dans les limites de la grille
        if 0 <= new_x < grid_width * grid_cell_size and 0 <= new_y < grid_height * grid_cell_size:
            self.rect.x = new_x
            self.rect.y = new_y
