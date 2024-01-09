import pygame
import time
import sys
import random
from Objet import BOB
from Objet import Nourriture
from Objet import CameraGroup
from Objet import Case
# from Objet import Tuile

GRID_WIDTH = 10
GRID_HEIGHT = 10
GRID_CELL_WIDTH, GRID_CELL_HEIGHT = 60, 30
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLANC = (0, 100, 0)
NOIR = (34, 139, 34)

# Coordonnées de la caméra
camera_x = 0  
camera_y = 0

GRID_CELL_SIZE = GRID_CELL_WIDTH*GRID_CELL_HEIGHT
global LISTX, LISTY
LISTX, LISTY, LIST = [], [], []


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('BOB LAND')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        bob_group = pygame.sprite.Group()
        self.Nourriture_group = pygame.sprite.Group()
        self.cameragroup = CameraGroup()

        for bob in range(5):
            new_bob = BOB(random.randrange(0, SCREEN_WIDTH-5),
                          random.randrange(0, SCREEN_HEIGHT-5), self.cameragroup)
            bob_group.add(new_bob)

        """nez_world = World()
        self.List = []"""

        for y in range(0, 20):
            for x in range(0, 20):
                # self.List.append((x, y))
                Case(x, y, self.cameragroup)

    def run(self):

        display = pygame.Surface((300, 300))
        while True:

            SPAWN_EVENT = pygame.USEREVENT + 1
            pygame.time.set_timer(SPAWN_EVENT, 2000)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # elif event.type == pygame.KEYDOWN:

                    # if event.key == pygame.K_LEFT:
                    #     # Déplacer la caméra vers la gauche
                    #     self.deplacer_camera(-40, 0)
                    # elif event.key == pygame.K_RIGHT:
                    #     # Déplacer la caméra vers la droite
                    #     self.deplacer_camera(40, 0)
                    # elif event.key == pygame.K_UP:
                    #     # Déplacer la caméra vers le haut
                    #     self.deplacer_camera(0, -40)
                    # elif event.key == pygame.K_DOWN:
                    #     # Déplacer la caméra vers le bas
                    #     self.deplacer_camera(0, 40)

                elif event.type == SPAWN_EVENT:
                    new_Nourriture = Nourriture(random.randrange(
                        0, SCREEN_WIDTH-5), random.randrange(0, SCREEN_HEIGHT-5), self.cameragroup)
                    self.Nourriture_group.add(new_Nourriture)

            self.cameragroup.update()
            self.cameragroup.custom_draw()

            # self.screen.blit(pygame.transform.scale(display, self.screen.get_size()), (0, 0))
            pygame.display.flip()
            self.clock.tick(20)


if __name__ == '__main__':
    game = Game()
    game.run()
