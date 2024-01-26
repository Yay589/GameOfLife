from typing import Any
import pygame
import random


class Nourriture(pygame.sprite.Sprite):
    def __init__(self,id):
        self.id=id
        self.type = "food"
        self.energy = 100
        self.alive = True
        
        self.image = pygame.image.load('data/images/apple.png').convert()
        self.image.set_colorkey((37, 43, 43))

        self.rect = self.image.get_rect()
        self.rect.center = list([0, 0])
        
        self.infos = {'type':self.type,'id':self.id,'energy':self.energy}

class BOB(pygame.sprite.Sprite):
    def __init__(self,id):
        self.id=id
        self.type = "bob"
        self.energy = 100
        self.alive = True

        self.sprites = []
        self.sprites.append(pygame.image.load('data/images/0.png').convert())
        self.sprites.append(pygame.image.load('data/images/1.png').convert())
        self.sprites.append(pygame.image.load('data/images/2.png').convert())
        self.sprites.append(pygame.image.load('data/images/3.png').convert())
        
        self.current_sprite = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = list([0, 0])

        self.infos = [self.type,self.id,self.energy]

