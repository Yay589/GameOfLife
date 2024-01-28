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
        
        self.sprites = [pygame.image.load(f'data/images/kirby1.{i}.png').convert() for i in range(9)]  
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = Bob.coordinates
        
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