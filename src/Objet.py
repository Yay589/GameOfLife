from typing import Any
import pygame
import random


class CameraGroup(pygame.sprite.Group):

    def __init__(self):

        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left': 200,
                               'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size(
        )[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size(
        )[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # self.ground_surf = pygame.image.load('data/images/ground.png').convert_alpha()
        # self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))
        # self.ground_surf =pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # parametre

        self.keyboard_speed = 15
        self.mouse_speed = 0.2

        # zoom
        self.zoom_scale = 1
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(
            self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(
            center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(
            self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]:
            self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.1

    def custom_draw(self):

        self.keyboard_control()
        self.zoom_keyboard_control()

        self.internal_surf.fill('white')

        # ground
        # ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        # self.internal_surf.blit(self.ground_surf,ground_offset)
        # grille= tuile()
        # tuile.setting_tuile(grille,self.ground_surf,self.offset.x-self.internal_offset.x,self.offset.y-self.internal_offset.y)

        # active elements
        for sprite in self.sprites():
            # sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            # order by y axe
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(
            self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)


# class Tuile(pygame.sprite.Sprite):
#     GRID_WIDTH = 10
#     GRID_HEIGHT = 10
#     GRID_CELL_WIDTH, GRID_CELL_HEIGHT = 60, 30
#     SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
#     BLANC = (0, 100, 0)
#     NOIR = (34, 139, 34)

#     def __init__(self):
#         super().__init__()
#         self.LIST = []
#         self.x = 0
#         self.y = 0
#         self.couleur = (0, 0, 0)

#         # self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

#     def setting_tuile(screen):
#         Grille = pygame.sprite.Group()
#         new_tuile = Tuile()
#         for i in range(new_tuile.GRID_WIDTH):
#             for j in range(new_tuile.GRID_HEIGHT):
#                 new_tuile.x = (i - j) * new_tuile.GRID_CELL_WIDTH
#                 new_tuile.y = (i + j) * new_tuile.GRID_CELL_HEIGHT
#                 if (i + j) % 2 == 0:
#                     new_tuile.couleur = new_tuile.NOIR
#                 else:
#                     new_tuile.couleur = new_tuile.BLANC

#                 points = [(new_tuile.x, new_tuile.y + new_tuile.GRID_CELL_HEIGHT), (new_tuile.x + new_tuile.GRID_CELL_WIDTH, new_tuile.y),
#                           (new_tuile.x + 2 * new_tuile.GRID_CELL_WIDTH, new_tuile.y + new_tuile.GRID_CELL_HEIGHT), (new_tuile.x + new_tuile.GRID_CELL_WIDTH, new_tuile.y + 2 * new_tuile.GRID_CELL_HEIGHT)]
#                 for i in range(4):
#                     new_tuile.LIST.append(points[i])
#                 new_tuile.draw.polygon(screen, new_tuile.couleur, points)


class Case(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)

        self.image = pygame.image.load('data/images/grass.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = [150 + x * 10 - y * 10, 100 + x * 5 + y * 5]


class Nourriture(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group):
        super().__init__(group)
        self.sprites = []
        self.sprites.append(pygame.image.load('data/images/apple.png'))
        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def update(self):
        self.image = self.sprites[self.current_sprite]


class BOB(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group):
        super().__init__(group)
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

    def bouger(self, grid_cell_size, listPoints, cx, cy):
        # Déplacement aléatoire en multiples de la taille de la cellule
        dx = random.randint(-1, 1) * grid_cell_size
        # Déplacement aléatoire en multiples de la taille de la cellule
        dy = random.randint(-1, 1) * grid_cell_size

        selection = [(self.rect.center[0]+cx + dx_, self.rect.center[1]+cy + dy_) for dx_ in [-dx, 0, dx]
                     for dy_ in [-dy, 0, dy]]
        posibilities = []
        for i in selection:
            if i in listPoints:
                posibilities.append(i)
        # print("selection = ", selection)
        # print("posibilities = ", posibilities)
        # print("listPoints = ", listPoints)
        point = random.choice(posibilities)
        new_x, new_y = point

        self.rect.x = new_x-cx
        self.rect.y = new_y-cy
