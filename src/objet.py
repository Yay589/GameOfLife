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
        self.energy=200

    def update(self):

        self.current_sprite += 1
        self.energy-=5
        
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        # assigning the next image of the animation
        self.image = self.sprites[self.current_sprite]

    def bouger(self):

        dx = random.randint(-20, 20)
        dy = random.randint(-20, 20)
        # To stay within the limits of the map:
        if self.rect.left + dx >= 0 and self.rect.right + dx <= 1280:
            self.rect.x += dx
        if self.rect.top + dy >= 0 and self.rect.bottom + dy <= 720:
            self.rect.y += dy
