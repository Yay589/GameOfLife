import sys
import pygame
from bob import Bob
from parametre import *

pygame.init()


pygame.font.init()

# Define the screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Your Game Title')

class Render:
    def __init__(self) :
        self.all_gameobject=pygame.sprite.Group()
        self.listObjects = []
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(N)]
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

        self.zoom_scale = 2
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def add_object(self, game_object):
        self.listObjects.append(game_object)


    def draw(self,pause):
        self.keyboard_control()
        self.zoom_keyboard_control()
        
        screen.fill((0,0,0))
        
        
        image_ground = pygame.image.load('data/images/ground.jpg')
        image_ground = pygame.transform.scale(image_ground, (1500, 700))
        screen.blit(image_ground, (0,0))
        
        
        for i in self.list_x_y:
            #screen.blit(self.image, i)
            vect_list = [x * self.zoom_scale for x in (self.rect.width ,self.rect.height)]
            image=pygame.transform.scale(self.image, vect_list)
            screen.blit(image, [(i[0]-self.offset.x)*self.zoom_scale,(i[1]-self.offset.y)* self.zoom_scale])

        for obj in self.all_gameobject:
            print(obj.rect.center)
            location=()
            location=obj.rect.center
            #screen.blit(obj.image, list(eval(k)))           
            vect_list_obj = [x * self.zoom_scale*obj.taille for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]
            image_obj=pygame.transform.scale(obj.image, vect_list_obj)
            #screen.blit(image_obj, [(obj.rect.x*10+205-self.offset.x)*self.zoom_scale,(obj.rect.y*5+170-self.offset.y)*self.zoom_scale])

            screen.blit(image_obj, [(157.5 + location[0] * 10 - location[1] * 10-self.offset.x)*self.zoom_scale
                                    ,(100 + location[0] * 5 + location[1] * 5-self.offset.y)*self.zoom_scale])
            if isinstance(obj, Bob):
                obj.image = obj.sprites[obj.current_sprite]

        font = pygame.font.Font(None, 36)
        text_render = font.render(f"The number of our residents: {len(allBobs)}", True, (0, 0, 0))
        screen.blit(text_render, (350,50))
        
        if pause:
            pause_image = pygame.image.load('data/images/pause.png')
            pause_image = pygame.transform.scale(pause_image, (300, 200))
            #pause_image.set_colorkey((255,255,255))
            screen.blit(pause_image, (250, 200))
            
            
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