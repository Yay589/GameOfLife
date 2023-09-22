import pygame
import time
import sys
import random
from objet import BOB
from objet import Nourriture

GRID_WIDTH = 100
GRID_HEIGHT = 100
GRID_CELL_SIZE = 10
SCREEN_WIDTH = GRID_WIDTH * GRID_CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_CELL_SIZE


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('BOB LAND')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        # Dessiner les lignes verticales de la grille
        for x in range(0, SCREEN_WIDTH, GRID_CELL_SIZE):
            pygame.draw.line(self.screen, (128, 128, 128),
                             (x, 0), (x, SCREEN_HEIGHT))

        # Dessiner les lignes horizontales de la grille
        for y in range(0, SCREEN_HEIGHT, GRID_CELL_SIZE):
            pygame.draw.line(self.screen, (128, 128, 128),
                             (0, y), (SCREEN_WIDTH, y))

    def run(self):

        Nourriture_group = pygame.sprite.Group()
        bob_group = pygame.sprite.Group()

        for bob in range(5):
            new_bob = BOB(random.randrange(0, GRID_WIDTH) * GRID_CELL_SIZE+GRID_CELL_SIZE/2,
                          random.randrange(0, GRID_HEIGHT) * GRID_CELL_SIZE+GRID_CELL_SIZE/2)
            bob_group.add(new_bob)

        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 2000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == SPAWN_EVENT:
                    new_Nourriture = Nourriture(random.randrange(0, GRID_WIDTH) * GRID_CELL_SIZE+GRID_CELL_SIZE/2,
                                                random.randrange(0, GRID_HEIGHT) * GRID_CELL_SIZE+GRID_CELL_SIZE/2)
                    Nourriture_group.add(new_Nourriture)

            pygame.display.flip()
            for bobs in bob_group:
                for nurri in Nourriture_group:
                    if pygame.sprite.collide_rect(bobs, nurri):
                        Nourriture_group.remove(nurri)

            for bob in bob_group:
                bob.bouger(GRID_WIDTH, GRID_HEIGHT, GRID_CELL_SIZE)

            self.screen.fill((0, 0, 0))
            self.draw_grid()  # Dessiner la grille
            bob_group.draw(self.screen)
            bob_group.update()
            Nourriture_group.draw(self.screen)
            self.clock.tick(20)
