import sys
import pygame
from bob import Bob
#from case import Case #En attente des modifications de celestine
#from nourriture import Nourriture

class BobSprite(pygame.sprite.Sprite,Bob):
    def __init__(self,Bob):
        super().__init__()
        self.energy=Bob.energy
        self.taille=Bob.energy/800+0.2
        self.gbob=Bob
        #self.sprites = []
        #self.sprites.append(pygame.image.load('data/images/0.png').convert())
        #self.sprites.append(pygame.image.load('data/images/1.png').convert())
        #self.sprites.append(pygame.image.load('data/images/2.png').convert())
        #self.sprites.append(pygame.image.load('data/images/3.png').convert())
        self.current_sprite = 0
        self.image = pygame.image.load('data/images/kirby.png')
        self.rect = self.image.get_rect()
        self.rect.center = Bob.coordinates
        self.sprites = [pygame.image.load(f'data/images/kirby1.{i}.png').convert() for i in range(9)]  

        self.current_sprite = 0
        self.animation_timer = pygame.time.get_ticks()  

    def update_position(self):
        self.rect.center = self.gbob.previousCoordinates
        
    #def update_animation(self,i):
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.animation_timer > 100: 
            self.animation_timer = now
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]