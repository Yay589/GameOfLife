import pygame
import time
import sys
import random
from Objet import BOB
from Objet import Nourriture

GRID_WIDTH = 10
GRID_HEIGHT = 10
GRID_CELL_WIDTH, GRID_CELL_HEIGHT = 60, 30
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLANC = (0, 100, 0)
NOIR = (34, 139, 34)

# Coordonnées de la caméra
camera_x = 0  # -(SCREEN_WIDTH//2)+GRID_CELL_WIDTH
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

    def dessiner_tuile(self, x, y, couleur):
        global LISTX, LISTY, LIST

        points = [(x, y + GRID_CELL_HEIGHT), (x + GRID_CELL_WIDTH, y),
                  (x + 2 * GRID_CELL_WIDTH, y + GRID_CELL_HEIGHT), (x + GRID_CELL_WIDTH, y + 2 * GRID_CELL_HEIGHT)]
        for i in range(4):
            LISTX.append(points[i][0])
            LISTY.append(points[i][1])
            LIST.append(points[i])

        pygame.draw.polygon(self.screen, couleur, points)
        # Dessiner un contour autour de la tuile
        # pygame.draw.lines(self.screen, NOIR, True, points, 1)

    def deplacer_camera(self, dx, dy):
        global camera_x, camera_y
        camera_x += dx
        camera_y += dy

    def run(self):
        while True:

            SPAWN_EVENT = pygame.USEREVENT + 1
            pygame.time.set_timer(SPAWN_EVENT, 2000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        # Déplacer la caméra vers la gauche
                        self.deplacer_camera(-40, 0)
                    elif event.key == pygame.K_RIGHT:
                        # Déplacer la caméra vers la droite
                        self.deplacer_camera(40, 0)
                    elif event.key == pygame.K_UP:
                        # Déplacer la caméra vers le haut
                        self.deplacer_camera(0, -40)
                    elif event.key == pygame.K_DOWN:
                        # Déplacer la caméra vers le bas
                        self.deplacer_camera(0, 40)
                elif event.type == SPAWN_EVENT:
                    new_Nourriture = Nourriture(random.randrange(min(LISTX), max(
                        LISTX))-camera_x, random.randrange(min(LISTY), max(LISTY))-camera_y)
                    Nourriture_group.add(new_Nourriture)

            self.screen.fill((255, 255, 255))  # fond Blanc

            # Dessiner la grille losange
            for i in range(GRID_WIDTH):
                for j in range(GRID_HEIGHT):
                    x = (i - j) * GRID_CELL_WIDTH - camera_x
                    y = (i + j) * GRID_CELL_HEIGHT - camera_y
                    if (i + j) % 2 == 0:
                        couleur = NOIR
                    else:
                        couleur = BLANC
                    self.dessiner_tuile(x, y, couleur)

            Nourriture_group = pygame.sprite.Group()
            bob_group = pygame.sprite.Group()

            for bob in range(5):
                position = random.choice(LIST)
                # BOB(random.randrange(min(LISTX), max(LISTX))-camera_x, random.randrange(min(LISTY), max(LISTY))-camera_y)
                new_bob = BOB(position[0]-camera_x, position[1]-camera_y)
                bob_group.add(new_bob)

            for bobs in bob_group:
                for nurri in Nourriture_group:
                    if pygame.sprite.collide_rect(bobs, nurri):
                        Nourriture_group.remove(nurri)

            for bob in bob_group:
                bob.bouger(GRID_CELL_SIZE, LIST, camera_x, camera_y)

            bob_group.draw(self.screen)
            bob_group.update()
            Nourriture_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(20)


if __name__ == '__main__':
    game = Game()
    game.run()
