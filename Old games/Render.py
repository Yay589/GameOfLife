import sys
import pygame
from random import *
import math
from parametre import *
from case import Case
from bob import Bob
from affichage import *
pygame.init()


pygame.font.init()

# Define the screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Your Game Title')

class Render:
    def __init__(self) :
        self.ball_x=0
        self.ball_y=0
        self.angle=0
        self.day_night=0
        self.sombre=200
        self.plat=5
        self.show = False
        self.show_energy=0
        self.game_running = False
        self.is_paused = False
        self.all_gameobject=pygame.sprite.Group()
        self.listObjects = []
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(N)]
        #self.random_values_for_tree = random.sample(self.list_x_y, 6)

        # num_points_to_select = N // 5 + 1
        # available_points = self.list_x_y.copy()
        # self.selected_points = []
        # for _ in range(num_points_to_select):
        #     random_point = random.choice(available_points)
        #     self.selected_points.append(random_point)
        #     available_points.remove(random_point)

        
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

        self.zoom_scale = 1.5
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
        # Contrôle du clavier pour déplacer l'écran
        self.keyboard_control()
        
        # Contrôle du clavier pour effectuer un zoom
        self.zoom_keyboard_control()

        # Écraser l'écran restant du tick précédent
        screen.fill((0, 0, 0))

        # Dessiner l'arrière-plan
        self.draw_background()

        # Dessiner le soleil
        self.draw_sun()

        # Dessiner l'île flottante
        self.draw_Floating_Island_Cliff()

        # Contrôle du clavier pour incliner
        self.zoom_keyboard_control()

        # Dessiner des éléments
        self.draw_cases()
        self.draw_objects()



        
        # for i in self.random_values_for_tree:
        #     image_tree = pygame.image.load('data/images/05.png')
        #     j=[(i[0]-self.offset.x)*self.zoom_scale,(i[1]-self.offset.y)* self.zoom_scale]
        #     image=pygame.transform.scale(image_tree, (50, 50))

        #     screen.blit(image,j)


        # Afficher l’énergie de Bob
        if self.show:
            font = pygame.font.Font(None, 36)
            text_show = font.render(f"Bob tu veux : {self.show_energy}", True, (0, 0, 0))
            screen.blit(text_show, (350, 100))

        # Afficher l'image de pause si le jeu est en pause
        if self.is_paused:
            image_pause = pygame.image.load('data/images/pause.png')
            image_pause.set_colorkey((255, 255, 255))
            image_pause = pygame.transform.scale(image_pause, (50, 50))
            screen.blit(image_pause, (375, 275))

        pygame.display.flip()
    
    def draw_background(self):
        image_ground = pygame.image.load('data/images/Ocean-and-Cloud.png')
        image_ground = pygame.transform.scale(image_ground, (1800,1200 ))
        image_ground.set_alpha(self.sombre)
        screen.blit(image_ground, (-500,-300))
    
    def draw_sun(self):
        image_ball = pygame.image.load('data/images/full.png')
        image_ball = pygame.transform.scale(image_ball, (100, 100))
        ball_rect = image_ball.get_rect()
        if not self.is_paused:
            self.angle += 0.02
            self.ball_x = 400 + 400 * math.cos(self.angle)
            self.ball_y = 250 + 200 * math.sin(self.angle)
        screen.blit(image_ball, (self.ball_x - ball_rect.width // 2,self.ball_y - ball_rect.height // 2))

    def draw_Floating_Island_Cliff(self):
        lenth_under=2*N * 10 * self.zoom_scale
        image_under = pygame.image.load('data/images/underground.png')
        image_under = pygame.transform.scale(image_under, (lenth_under,0.7*lenth_under ))
        x_under=150 - N * 10+ N*0.5-self.rect.width/2
        y_under=100 + N/2 * self.plat + N/2 *self.plat
        screen.blit(image_under,  [(x_under-self.offset.x)*self.zoom_scale,(y_under-self.offset.y)* self.zoom_scale])

    def show_value(self,mouse_x, mouse_y,real_location_x,real_location_y):
        for obj in self.all_gameobject:
            vect_list_obj = [x * self.zoom_scale*obj.taille for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]
            location=()
            location=obj.rect.center
            real_location_x=(150 + location[0] * 10 - location[1] * 10-self.offset.x)*self.zoom_scale-vect_list_obj[0]/2
            real_location_y=(100 + location[0] * self.plat + location[1] * self.plat-self.offset.y)*self.zoom_scale-vect_list_obj[1]/2
            
            obj.width= pygame.Surface.get_width(obj.image)
            obj.height=pygame.Surface.get_height(obj.image)
            

            # Check if the mouse click is within the bounds of the obj
            if (
                real_location_x < mouse_x < real_location_x + obj.width * self.zoom_scale
                and real_location_y < mouse_y < real_location_y + obj.height * self.zoom_scale
            ):
                self.show_energy=obj.energy
    
    def draw_cases(self):
        for i in self.list_x_y:
            #screen.blit(self.image, i)
            vect_list = [x * self.zoom_scale for x in (self.rect.width ,self.rect.height*(self.plat/5))]
            image=pygame.transform.scale(self.image, vect_list)

            case_locattion=[(i[0]-self.offset.x-self.rect.width/2)*self.zoom_scale
                                ,(i[1]-self.offset.y)* self.zoom_scale]
            screen.blit(image, case_locattion)
            
    
    def draw_objects(self):
        event = pygame.event.get()
        for obj in self.all_gameobject:

            location=()
            location=obj.rect.center
            #screen.blit(obj.image, list(eval(k)))           
            vect_list_obj = [x * self.zoom_scale*obj.taille for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]
            image_obj=pygame.transform.scale(obj.image, vect_list_obj)
            #screen.blit(image_obj, [(obj.rect.x*10+205-self.offset.x)*self.zoom_scale,(obj.rect.y*5+170-self.offset.y)*self.zoom_scale])
            
            real_location_x=(150 + location[0] * 10 - location[1] * 10-self.offset.x)*self.zoom_scale-vect_list_obj[0]/2
            real_location_y=(100 + location[0] * self.plat + location[1] * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj[1]*(1/2)
            real_location=[real_location_x,real_location_y]

           
            screen.blit(image_obj, real_location)
        font = pygame.font.Font(None, 36)
        text_render = font.render(f"The number of our residents: {len(allBobs)}", True, (0, 0, 0))
        screen.blit(text_render, (350,50))

        if len(allBobs) != 0:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.show=True
                    self.show_value(mouse_x, mouse_y,real_location_x,real_location_y)
   
    
    def draw_start(self):
        self.keyboard_control()
        self.zoom_keyboard_control()
        
        screen.fill((0,0,0))
        image_ground = pygame.image.load('data/images/Ocean-and-Cloud.png')
        image_ground = pygame.transform.scale(image_ground, (1800,1200 ))
        screen.blit(image_ground, (-500,-300))
        button_color = (0, 255, 0)
        button_width, button_height = 200, 50
        button_x, button_y = (SCREEN_WIDTH - button_width) // 2, (SCREEN_HEIGHT - button_height) // 2
        font = pygame.font.Font(None, 36)
        text = font.render("Start Game", True, (0, 0, 0))
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                    self.game_running = True

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