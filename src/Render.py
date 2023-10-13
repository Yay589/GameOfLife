import pygame

class Render:
    def __init__(self) -> None:
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(self.n) for y in range(self.m)]
        self.image = pygame.image.load('data/images/grass.png').convert()
        self.image.set_colorkey((0, 0, 0))
        for i in self.list_x_y:
            self.rect = self.image.get_rect()
            self.rect.center = i
        