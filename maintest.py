import pygame
from World import World
from random import *
from parametre import *
from math import trunc
from nourriture import Nourriture
from case import Case
from bob import Bob
from affichage import *
from fonction_mix import *
pygame.init()


pygame.font.init()

# Define the screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Your Game Title')

class Game:
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

        self.zoom_scale = 1
        self.internal_surf_size = (2500, 2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def add_object(self, game_object):
        self.listObjects.append(game_object)


    def draw(self):
        self.keyboard_control()
        self.zoom_keyboard_control()
        
        screen.fill((255, 255, 255))
        for i in self.list_x_y:
            #screen.blit(self.image, i)
            vect_list = [x * self.zoom_scale for x in (self.rect.width ,self.rect.height)]
            image=pygame.transform.scale(self.image, vect_list)
            screen.blit(image, [(i[0]-self.offset.x)*self.zoom_scale,(i[1]-self.offset.y)* self.zoom_scale])

        for obj in self.all_gameobject:
            print(obj.rect.center)
            #screen.blit(obj.image, list(eval(k)))           
            vect_list_obj = [x * self.zoom_scale for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]
            image_obj=pygame.transform.scale(obj.image, vect_list_obj)
            screen.blit(image_obj, [(obj.rect.x*10+210-self.offset.x)*self.zoom_scale,(obj.rect.y*5+170-self.offset.y)*self.zoom_scale])
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
        
        
class BOB_GameObject(pygame.sprite.Sprite,Bob):
    def __init__(self,Bob):
        super().__init__()
        self.gbob=Bob
        self.sprites = []
        self.sprites.append(pygame.image.load('data/images/0.png').convert())
        self.sprites.append(pygame.image.load('data/images/1.png').convert())
        self.sprites.append(pygame.image.load('data/images/2.png').convert())
        self.sprites.append(pygame.image.load('data/images/3.png').convert())
        self.current_sprite = 0
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = Bob.coordonnee


    def update_position(self):
        self.rect.center = self.gbob.coordonnee

g=Game()
print(g.list_x_y)




for i in range(N-1):
        allBobs.append(Bob(coord = (randint(0,N-1),randint(0,N-1))))
allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(2*N)]


for bob in allBobs:
    g.all_gameobject.add(BOB_GameObject(bob))


bob_ex = Bob( bobEnergy=bobMaxE, coord = (0,0))
allBobs.append(bob_ex)


running = True
font = pygame.font.Font(None, 36)
text = font.render("Press S key to save and continue", True,'black')
save_option_shown = False
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    g.draw()
    



    for b in allBobs:
        if(not b.reproduction()):
            if(not b.manger()):
                b.bouger()

    g.all_gameobject.empty()

    for bob in allBobs:
        g.all_gameobject.add(BOB_GameObject(bob))


        for j in g.all_gameobject:
            j.update_position()
        
    
    clock.tick(20)
    
pygame.quit()