import pygame, os, pickle
from World import World
from collections import defaultdict
from Object import *


# Define the screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game Of life')

class Render:
    def __init__(self, n, m) -> None:
        self.world = World(n,m)
        self.n = n
        self.m = m
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(self.n) for y in range(self.m)]
        self.image = pygame.image.load('data/images/grass.png').convert()
        self.image.set_colorkey((0, 0, 0))
        for i in self.list_x_y:
            self.rect = self.image.get_rect()
            self.rect.center = i
            
            
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.camera_borders = {'left': 200,'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)
        
        self.keyboard_speed = 15
        self.mouse_speed = 0.2

        self.zoom_scale = 1
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
    
    def draw(self):
        self.keyboard_control()
        self.zoom_keyboard_control()
        
        screen.fill((255, 255, 255))
        for i in self.list_x_y:
            #screen.blit(self.image, i)
            vect_list = [x * self.zoom_scale for x in (self.rect.width ,self.rect.height)]
            image=pygame.transform.scale(self.image, vect_list)
            screen.blit(image, [(i[0]-self.offset.x)*self.zoom_scale,(i[1]-self.offset.y)* self.zoom_scale])

        for k, v in self.world.world.items():
            for obj in v:
                #screen.blit(obj.image, list(eval(k)))           
                vect_list_obj = [x * self.zoom_scale for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]
                image_obj=pygame.transform.scale(obj.image, vect_list_obj)
                screen.blit(image_obj, [(list(eval(k))[0]-self.offset.x)*self.zoom_scale,(list(eval(k))[1]-self.offset.y)*self.zoom_scale])
                if (obj.type == "bob"):
                    obj.current_sprite = 0 if  obj.current_sprite == 3 else obj.current_sprite+1
                    obj.image = obj.sprites[obj.current_sprite]
                
        pygame.display.flip()
    
   
    
    
    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_RIGHT]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_UP]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_DOWN]:
            self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            self.zoom_scale += 0.1
        if keys[pygame.K_x]:
            self.zoom_scale -= 0.1
            
    def save(self):
        # Chemin du fichier save.txt
        fichier_save = 'data/save.txt'

        #Si on save, on supprime les ancienne données
        if os.path.exists(fichier_save):
            os.remove(fichier_save)
        
        info_dict = {k:v.infos for k,v in self.world.world.items()}
        
        # Utilise pickle pour sauvegarder le dictionnaire dans le fichier crée.
        with open(fichier_save, 'wb') as fichier:
            pickle.dump(info_dict, fichier)

        #print("Sauvegarde réussie dans", fichier_save)


    def load(self):
        # Chemin du fichier save.txt
        fichier_save = 'data/save.txt'

        try:
            # Utilise pickle pour charger le dictionnaire depuis le fichier
            with open(fichier_save, 'rb') as fichier:
                info_dict = pickle.load(fichier)

            self.world = defaultdict(list)
                               
            
            for k,v in info_dict.items():              
                for infos in v:
                    if infos[type] == "food":
                        self.world[k].append(Nourriture(infos['id']))
                        
                    else:
                        this_bob = BOB(infos['id'])
                        this_bob.energy = infos['energy']
                        self.world[k].append(this_bob)
            
            print("Chargement réussi depuis", fichier_save)
            print("Contenu du dictionnaire chargé :", self.dictionnaire)
        except FileNotFoundError:
            print("Le fichier de sauvegarde n'existe pas. Impossible de charger.")

