import sys
import pygame
from bob import Bob
#from case import Case #En attente des modifications de celestine
#from nourriture import Nourriture

class BobSprite(pygame.sprite.Sprite,Bob):
    def __init__(self,Bob):
        super().__init__()
        self.taille=Bob.energy/800+0.3
        self.gbob=Bob
        self.sprites = []
        self.sprites.append(pygame.image.load('data/images/0.png').convert())
        self.sprites.append(pygame.image.load('data/images/1.png').convert())
        self.sprites.append(pygame.image.load('data/images/2.png').convert())
        self.sprites.append(pygame.image.load('data/images/3.png').convert())
        self.current_sprite = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = Bob.coordonnee


    def update_position(self):
        self.rect.center = self.gbob.coordonnee
"""
class FoodSprite(pygame.sprite.Sprite,Nourriture):
    def __init__(self,Nourriture):
        super().__init__()
        self.taille=0.42
        self.gfood=Nourriture
        self.image = pygame.image.load('data/images/apple.png').convert()
        self.rect = self.image.get_rect()
        self.rect.center = Nourriture.coordonnee
        self.image.set_colorkey((37, 43, 43))


    def update_position(self):
        self.rect.center = self.gfood.coordonnee
        self.image.set_colorkey((37, 43, 43))
"""