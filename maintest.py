import pygame
from random import *
import math
from parametre import *
import parametre
from case import *
from bob import Bob
import pickle
import subprocess
import os
import sys
from affichage import *
from statistiques import *
import cProfile


# import time

pygame.init()


pygame.font.init()

# Define the screen dimensions
SCREEN_WIDTH_FULL, SCREEN_HEIGHT_FULL = pygame.display.Info().current_w, pygame.display.Info().current_h
fullscreen = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BOB_LAND')

class Button_text:
    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image_back = pygame.image.load('data/images/background/background1.png')
        self.image_back = pygame.transform.scale(self.image_back, (self.width, self.height))

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height))
        screen.blit(self.image_back, (self.x,self.y))
        
        
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), 
                        self.y + round(self.height/2) - round(text.get_height()/2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class Game:
    def __init__(self) :
        self.action_button = Button_text(25, 100, 200, 60, 'Version console')
        self.setting_frame=0
        self.selected_index = -1
        self.selected_index_start=-1
        self.nom_sauvegarde=""
        self.start_anime=False
        self.tick=30
        self.tick_by_day=15
        self.costum_number=8
        self.ball_x=0
        self.ball_y=0
        self.angle=0
        self.day_night=0
        self.sombre=200
        self.plat=5
        self.costum=0
        self.costum_case=0
        self.active=False
        self.show = False
        self.dragging = False
        self.guid = False
        self.setting = False
        self.show_energy=0
        self.game_running = False
        self.is_paused = False
        self.showbroad = False
        self.fullscreen= False
        self.save=False
        self.change=False
        self.grass_change=False
        self.all_gameobject=pygame.sprite.Group()
        self.listObjects = []
        self.linital_position = []
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(M)]
        
        self.random_case=[]
        
        #self.random_values_for_tree = random.sample(self.list_x_y, 6)

        # num_points_to_select = N // 5 + 1
        # available_points = self.list_x_y.copy()
        # self.selected_points = []
        # for _ in range(num_points_to_select):
        #     random_point = random.choice(available_points)
        #     self.selected_points.append(random_point)
        #     available_points.remove(random_point)

        self.img_appel = pygame.image.load('data/images/apple.png').convert()
        self.image = pygame.image.load('data/images/grass0.png').convert()
        self.image.set_colorkey((0, 0, 0))
        for i in self.list_x_y:
            self.rect = self.image.get_rect()
            self.rect.center = i

        self.dragging_offset_x=0

        self.dragging_offset_y=0

        self.image_broad = pygame.image.load('data/images/broad.png')

        self.image_broad.set_colorkey((255, 255, 255))

        self.image_broad = pygame.transform.scale(self.image_broad, (256, 128))

        self.image_broad_rect = self.image_broad.get_rect()

        self.line_color = (0,0,0)


        self.image_ball = pygame.image.load('data/images/full.png')
        self.image_ball = pygame.transform.scale(self.image_ball, (100, 100))
        self.ball_rect = self.image_ball.get_rect()

        self.image_ground=[]
        for frame in range(0,41):
            image_ground = pygame.image.load(f'data/images/background/background{frame}.png')
            image_ground = pygame.transform.scale(image_ground, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.image_ground.append(image_ground)
        


        self.line_width = 5
        self.line_padding = 40
        self.max_data_points = 20  # 最大数据点数

        self.data = []
            
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.camera_borders = {'left': SCREEN_HEIGHT,'right': SCREEN_HEIGHT, 'top': SCREEN_WIDTH, 'bottom': SCREEN_WIDTH}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        
        self.keyboard_speed = 10
        self.mouse_speed = 0.2

        self.zoom_scale = 3 
        # self.internal_surf_size = (SCREEN_HEIGHT, SCREEN_WIDTH)
        # self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        # self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        # self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        # self.internal_offset = pygame.math.Vector2()
        # self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        # self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
        self.vect_list = [(x * self.zoom_scale) for x in (24 ,12*(self.plat/5))]
        self.image=pygame.transform.scale(self.image, self.vect_list)

    def add_object(self, game_object):
        self.listObjects.append(game_object)


    def draw(self,walk_i):
        

        #if walk_i%2:
        # Contrôle du clavier pour déplacer l'écran
        self.keyboard_control()
        
        # Contrôle du clavier pour effectuer un zoom
        self.zoom_keyboard_control()

    
        # Écraser l'écran restant du tick précédent
        screen.fill((0, 0, 0))

        # Dessiner l'arrière-plan
        self.draw_background(walk_i)

        # Dessiner le soleil
        self.draw_sun()

    # Dessiner l'île flottante
    #self.draw_Floating_Island_Cliff()

        # Contrôle du clavier pour incliner
        self.tilt_keyboard_control()

    # Dessiner des éléments
        if self.costum_case==5:
            self.draw_lignes()
        if not (self.costum_case==5):
            self.draw_cases()

        self.draw_objects(walk_i)
        #if walk_i%2:
        self.draw_food()

        self.show_broad()

        self.draw_info()

        self.draw_restart()

        self.action_button.draw(screen)
        
        self.draw_menu()
        
        self.draw_summary_graph(walk_i)
        
        # for i in self.random_values_for_tree:
        #     image_tree = pygame.image.load('data/images/05.png')
        #     j=[(i[0]-self.offset.x)*self.zoom_scale,(i[1]-self.offset.y)* self.zoom_scale]
        #     image=pygame.transform.scale(image_tree, (50, 50))

        #     screen.blit(image,j)


        # Afficher l’énergie de Bob

        # Afficher l'image de pause si le jeu est en pause
        if self.is_paused:

            image_pause = pygame.image.load('data/images/pause.png')

            image_pause.set_colorkey((255, 255, 255))

            image_pause = pygame.transform.scale(image_pause, (50, 50))

            screen.blit(image_pause, (SCREEN_WIDTH-265, 50))
        
        self.draw_setting()
        

        pygame.display.flip()
    



    def draw_guid(self):

        guid_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        guid_surface.fill((128, 128, 128, 128))
        font = pygame.font.Font(None, 24)
        lines = [
            "Welcome to the guidance interface.",
            "Exit guidance menu : same bouton (i)"
            "Naviaguate though the map : arrow keys",
            "Zoom in : 'c' - Zoom out 'x'"
            "Adjust map's orientation 'w' - 's' "
            "Pause the game : space bar",
            "Infomation board for a specific bob : Press 'b' then select a bob ",
            "Move the information board : drag it with the mouse"
        ]

        y_position = SCREEN_HEIGHT // 4  

        for line in lines:
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            guid_surface.blit(text, text_rect)
            y_position += text_rect.height + SCREEN_HEIGHT // 25
        screen.blit(guid_surface, (0, 0))


    def draw_background(self, frame):
        self.image_ground[frame%41] = pygame.transform.scale(self.image_ground[frame%41], (SCREEN_WIDTH, SCREEN_HEIGHT))
        #self.image_ground[frame%41].set_alpha(self.sombre)
        screen.blit(self.image_ground[frame%41], (0, 0))
    
    def draw_sun(self):
        
        if not self.is_paused:
            self.angle += 0.02
            self.ball_x = 400 + 400 * math.cos(self.angle)
            self.ball_y = 250 + 200 * math.sin(self.angle)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.ball_x < mouse_x < self.ball_x + 100 and self.ball_y < mouse_y < self.ball_y + 100:
                self.image_ball = pygame.image.load('data/images/full1.png')
                self.image_ball = pygame.transform.scale(self.image_ball, (100*self.zoom_scale, 100*self.zoom_scale))
                
        screen.blit(self.image_ball, (self.ball_x - self.ball_rect.width // 2,self.ball_y - self.ball_rect.height // 2))

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
            


    def show_broad(self):

        if self.showbroad :

            screen.blit(self.image_broad, self.image_broad_rect)

            font = pygame.font.Font(None, 20)

            text_show = font.render(f"Energy: {self.show_energy}", True, (0, 0, 0))

            screen.blit(text_show, self.image_broad_rect.move(15, 15))

            text_render = font.render(f"Mass: {len(allBobs)}", True, (0, 0, 0))

            screen.blit(text_render, self.image_broad_rect.move(15, 45))


    def draw_info(self):        
        if self.guid:

            self.draw_guid()

        image_info = pygame.image.load('data/images/info.png')

        image_info.set_colorkey((255, 255, 255))

        image_info = pygame.transform.scale(image_info, (50, 50))

        screen.blit(image_info, (SCREEN_WIDTH-125, 50))

    def draw_skip(self):        
        
        image_skip = pygame.image.load('data/images/skip.png')

        image_skip = pygame.transform.scale(image_skip, (50, 50))

        screen.blit(image_skip, (SCREEN_WIDTH-125, 50))
        
 


    def draw_restart(self):        

        image_restart = pygame.image.load('data/images/restart.png')

        image_restart.set_colorkey((255, 255, 255))

        image_restart = pygame.transform.scale(image_restart, (50, 50))

        screen.blit(image_restart, (SCREEN_WIDTH-195, 50))
    

    def draw_setting(self):        

        image_setting = pygame.image.load('data/images/setting.png')

        image_setting.set_colorkey((255, 255, 255))

        image_setting = pygame.transform.scale(image_setting, (50, 50))

        screen.blit(image_setting, (SCREEN_WIDTH-100, SCREEN_HEIGHT-100))

        if self.setting :
            if self.setting_frame < 5:
                self.setting_frame+=1
                image_setting_a = pygame.image.load(f'data/images/setting/setting{self.setting_frame}.png')
                image_setting_a = pygame.transform.scale(image_setting_a, (8*SCREEN_HEIGHT//9,SCREEN_HEIGHT))
                screen.blit(image_setting_a, ((SCREEN_WIDTH - 8 * SCREEN_HEIGHT // 9) // 2, 0))
            
            
            else:
                image_setting_a = pygame.image.load(f'data/images/setting/setting{5}.png')
                image_setting_a = pygame.transform.scale(image_setting_a, (8*SCREEN_HEIGHT // 9, SCREEN_HEIGHT))
                screen.blit(image_setting_a, ((SCREEN_WIDTH - 8 * SCREEN_HEIGHT // 9) // 2, 0))

                font = pygame.font.Font(None, int(24*(SCREEN_HEIGHT/600)))
                lines2 = [
                    f"Avergage Values : ",
                    f"Speed :{avgSpeed()}",
                    f"Perception :{avgPerception()}",
                    f"Memmory :{avgMemory()}",
                    f"Mass :{avgMass()}",
                    f"Energy:{avgEnergy()}",
                    f"Number of bobs:",
                    f"Total :{nbBobs()}",
                    f"Sick :{nbBobs_malade()}",
                    f"Educated :{nbBobs_educated()}"
                ]
                lines = [
                    f"Number of ticks in a day:{self.tick_by_day}",
                    f"Energy contained in a cake:{foodE}",
                    f"Width:{N}",
                    f"Length:{M}",
                    f"Bob custom:{self.costum}",
                    f"Case custom:{self.costum_case}"
                    f"SCREEN_WIDTH:{SCREEN_WIDTH}",
                    f"SCREEN_HEIGHT:{SCREEN_HEIGHT}",
                ]

                deplace=SCREEN_HEIGHT//8
                
                # up = pygame.image.load(f'data/images/setting/up.png')
                # up = pygame.transform.scale(up, (50,50))
                # screen.blit(up, (SCREEN_WIDTH/6+40, 370))
                
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_n]:
                    if self.selected_index < 7 :
                        self.selected_index += 0.5
                    else:
                        self.selected_index=-1
                    

                # Blit each line onto the text surface with or without highlighting
                for i, line in enumerate(lines):
                    text = font.render(line, True, (255, 255, 255))  # Set text color to white
                    text_rect = text.get_rect(topleft=((SCREEN_WIDTH - 8 * SCREEN_HEIGHT // 9) // 2+150*SCREEN_HEIGHT/600, deplace))
                    screen.blit(text, text_rect.topleft)
                    if text_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                        self.selected_index=i

                    # Check if the line is selected, and draw a gray rectangle behind it
                    if int(self.selected_index) == i:
                        pygame.draw.rect(screen, (169, 169, 169), text_rect, 2)  # Highlight with a gray rectangle
                    
                    deplace += 20*(SCREEN_HEIGHT/600)  # Move to the next line
                    
                for i, line in enumerate(lines2):
                    text = font.render(line, True, (255, 255, 255))  # Set text color to white
                    text_rect = text.get_rect(topleft=((SCREEN_WIDTH - 8 * SCREEN_HEIGHT // 9) // 2+150*SCREEN_HEIGHT/600, 140+deplace))
                    screen.blit(text, text_rect.topleft)
                    if text_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                        self.selected_index=i

                    # Check if the line is selected, and draw a gray rectangle behind it
                    if int(self.selected_index) == i:
                        pygame.draw.rect(screen, (169, 169, 169), text_rect, 2)  # Highlight with a gray rectangle
                    
                    deplace += 20*(SCREEN_HEIGHT/600)  # Move to the next line
                
                #self.draw_statistics()
            
        
        else:
            if self.setting_frame > 0:
                self.setting_frame-=1
                image_setting_a = pygame.image.load(f'data/images/setting/setting{self.setting_frame}.png')
                image_setting_a = pygame.transform.scale(image_setting_a, (8*SCREEN_HEIGHT // 9,SCREEN_HEIGHT))
                screen.blit(image_setting_a, ((SCREEN_WIDTH - 8 * SCREEN_HEIGHT // 9) // 2, 0))
                    


    def draw_summary_graph(self,frame):
        if frame%self.tick_by_day==0:
            new_data_point = avgEnergy()
            self.data.append(new_data_point)

            # 保持数据点数量不超过最大值
            if len(self.data) > self.max_data_points:
                self.data.pop(0)

        width=400
        height=300
        # 绘制折线图
        for i in range(len(self.data) - 1):
            x1 = self.line_padding + i * (width - 2 * self.line_padding) // (self.max_data_points - 1)
            y1 = height - (self.data[i] * (height - 2 * self.line_padding) // max(self.data)) - self.line_padding

            x2 = self.line_padding + (i + 1) * (width - 2 * self.line_padding) // (self.max_data_points - 1)
            y2 = height - (self.data[i + 1] * (height - 2 * self.line_padding) // max(self.data)) - self.line_padding


            pygame.draw.line(screen, self.line_color, (x1, y1), (x2, y2), self.line_width)
    
    def draw_lignes(self):
        # i = 0
        # j = 0
        # x_y_1 = [0,0]
        # x_y_2 = [150 - (N-1) * 10, 100 + (N-1) * 5]
        # x_y_3 = [150 + (N-1) * 10 , 100 + (N-1) * 5 ]
        # x_y_4 = [150 + (N-1) * 10 - (N-1) * 10, 100 + (N-1) * 5 + (N-1) * 5]

        # case_location1 = [(x_y_1[0] - self.offset.x - self.rect.width/2) * self.zoom_scale,
        #                 (x_y_1[1] - self.offset.y) * self.zoom_scale]

        # case_location2 = [(x_y_2[0] - self.offset.x - self.rect.width/2) * self.zoom_scale,
        #                 (x_y_2[1] - self.offset.y) * self.zoom_scale]

        # case_location3 = [(x_y_3[0] - self.offset.x - self.rect.width/2) * self.zoom_scale,
        #                 (x_y_3[1] - self.offset.y) * self.zoom_scale]

        # case_location4 = [(x_y_4[0] - self.offset.x - self.rect.width/2) * self.zoom_scale,
        #                 (x_y_4[1] - self.offset.y) * self.zoom_scale]

        # diamond_points = [
        #     (case_location3[0], case_location3[1] ),
        #     (case_location1[0], case_location1[1] ),
        #     (case_location2[0], case_location2[1] ),
        #     (case_location4[0], case_location4[1] )
        # ]

        #pygame.draw.polygon(screen, (0, 0, 255), diamond_points)
        for i in range(1,M+1):
            x_y_1=[145 - i * 10, 95 + i * 5]
            x_y_2=[145 + (N) * 10 - i * 10, 95 + (N) * 5 + i * 5]
            case_locattion1=[(x_y_1[0]-self.offset.x-self.rect.width/2)*self.zoom_scale
                                ,(x_y_1[1]-self.offset.y)* self.zoom_scale]
            case_locattion2=[(x_y_2[0]-self.offset.x-self.rect.width/2)*self.zoom_scale
                                ,(x_y_2[1]-self.offset.y)* self.zoom_scale]
            pygame.draw.line(screen, self.line_color, (case_locattion1[0]+12,case_locattion1[1]), (case_locattion2[0]+12, case_locattion2[1]), 2)
        for j in range(1,N+1):
            x_y_1=[145 + j * 10 , 95 + j * 5 ]
            x_y_2=[145 + j * 10 - (M) * 10, 95 + j * 5 + (M) * 5]
            case_locattion1=[(x_y_1[0]-self.offset.x-self.rect.width/2)*self.zoom_scale
                                ,(x_y_1[1]-self.offset.y)* self.zoom_scale]
            case_locattion2=[(x_y_2[0]-self.offset.x-self.rect.width/2)*self.zoom_scale
                                ,(x_y_2[1]-self.offset.y)* self.zoom_scale]
            pygame.draw.line(screen, self.line_color, (case_locattion1[0]+12,case_locattion1[1]), (case_locattion2[0]+12, case_locattion2[1]), 2)
        

    def draw_cases(self):
        if self.change:
            self.vect_list.clear()
            self.vect_list = [(x * self.zoom_scale) for x in (24 ,12*(self.plat/5))]
            self.image = pygame.image.load(f'data/images/grass{self.costum_case}.png')
            self.image=pygame.transform.scale(self.image, self.vect_list)
            self.change=False
        for value , j in zip(self.list_x_y, self.random_case):
            # diamond_points = [(case_locattion [0], case_locattion [0]+24), (case_locattion [1], case_locattion [1]+12), (200, 350), (50, 200)]
            # pygame.draw.polygon(screen, (0, 0, 255), diamond_points)
            #self.image.set_alpha(j+180) 
            case_locattion=[(value[0]-self.offset.x-self.rect.width/2)*self.zoom_scale
                                ,(value[1]-self.offset.y)* self.zoom_scale]
            if -40*(self.zoom_scale/1.5)< case_locattion [0] and case_locattion [0] < SCREEN_WIDTH and -40*(self.zoom_scale/1.5) < case_locattion [1] and case_locattion [1] <SCREEN_HEIGHT:   
                screen.blit(self.image, case_locattion)
        
    
    def draw_objects(self,walk_i):
        for obj in self.all_gameobject:

            location=()
            location=obj.gbob.previousCoordinates
            #screen.blit(obj.image, list(eval(k)))
            
            #screen.blit(image_obj, [(obj.rect.x*10+205-self.offset.x)*self.zoom_scale,(obj.rect.y*5+170-self.offset.y)*self.zoom_scale])
            #obj.update()
            
                


            x=obj.gbob.coordinates[0]-obj.gbob.previousCoordinates[0]
            y=obj.gbob.coordinates[1]-obj.gbob.previousCoordinates[1]

            # if (self.gbob.previousCoordinates[1]- self.gbob.coordinates[1])*(self.gbob.previousCoordinates[0]- self.gbob.coordinates[0])<0:
            #     self.image = pygame.image.load(f'data/images/walking/walking{walk_i%10+1}.png')
            # else:

            # if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #     #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #     obj.image = pygame.image.load(f'data/images/walking/walking{walk_i%10+1}.png') 
            # else:
            #     #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #     obj.image = pygame.image.load(f'data/images/walking1/walking{walk_i%10+1}.png')
            vect_list_obj = [x * self.zoom_scale*obj.taille*0.4 for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]      
            vect_list_obj_searching = [x * self.zoom_scale*0.08 for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]

            # if self.costum%self.costum_number == 1:
            #     if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #     #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking20/walking20{walk_i%10+1}.png') 
            #     else:
            #         #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking21/walking21{walk_i%10+1}.png')      
            #     vect_list_obj[0]*=0.7

            # if self.costum%self.costum_number == 2:
            #     if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #     #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking30/walking30{walk_i%10+1}.png') 
            #     else:
            #         #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking31/walking30{walk_i%10+1}.png')      
            #     vect_list_obj[0]*=0.8

            # if self.costum%self.costum_number == 3:
            #     if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #     #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking40/walking40{walk_i%10+1}.png') 
            #     else:
            #         #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking41/walking40{walk_i%10+1}.png')      
            #     vect_list_obj[0]*=0.9

            # if self.costum%self.costum_number == 4:
            #     if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #     #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking50/walking50{walk_i%10}.png') 
            #     else:
            #         #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking51/walking50{walk_i%10}.png')      
            #     vect_list_obj[0]*=0.9

            # if self.costum%self.costum_number == 5:
            #     if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #     #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking60/walking60{walk_i%10}.png') 
            #     else:
            #         #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking61/walking60{walk_i%10}.png')      

            # if self.costum%self.costum_number == 6:
            #     if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #     #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking70/walking70_{walk_i%10+1}.png') 
            #     else:
            #         #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking71/walking70_{walk_i%10+1}.png')      
            #     vect_list_obj[0]*=0.7
            #     vect_list_obj[1]*=0.7

            # if self.costum%self.costum_number == 7:
            #     if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #     #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking80/walking80_{walk_i%10+1}.png') 
            #     else:
            #         #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/walking81/walking80_{walk_i%10+1}.png')      
            #     vect_list_obj[0]*=0.7

            if obj.gbob.tribe == 1:
                if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
                #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
                    obj.image = pygame.image.load(f'data/images/walking20/walking20{walk_i%10+1}.png') 
                else:
                    #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
                    obj.image = pygame.image.load(f'data/images/walking21/walking21{walk_i%10+1}.png')      
    

            if obj.gbob.tribe == 2:
                if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
                #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
                    obj.image = pygame.image.load(f'data/images/walking30/walking30{walk_i%10+1}.png') 
                else:
                    #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
                    obj.image = pygame.image.load(f'data/images/walking31/walking30{walk_i%10+1}.png')      

            if obj.gbob.tribe == 3:
                if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
                #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
                    obj.image = pygame.image.load(f'data/images/walking40/walking40{walk_i%10+1}.png') 
                else:
                    #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
                    obj.image = pygame.image.load(f'data/images/walking41/walking40{walk_i%10+1}.png')      

            if obj.gbob.tribe == 4:
                if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
                #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
                    obj.image = pygame.image.load(f'data/images/walking50/walking50{walk_i%10}.png') 
                else:
                    #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
                    obj.image = pygame.image.load(f'data/images/walking51/walking50{walk_i%10}.png')      
            
            

            # if obj.action== MANGER :
            #     obj.image = pygame.image.load(f'data/images/eating/eating{(walk_i%self.tick_by_day)%10+1}.png')
            
            
            #     if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
            #         #image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/searching/walking{walk_i%10+1}.png') 
            #     else:
            #         #image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
            #         obj.image = pygame.image.load(f'data/images/searching1/walking{walk_i%10+1}.png')
                    
            
            
            
            real_location_x=(150 + (location[0]+ x*(walk_i%self.tick_by_day)/self.tick_by_day) * 10 - (location[1]+ y*(walk_i%self.tick_by_day)/self.tick_by_day) * 10-self.offset.x)*self.zoom_scale-vect_list_obj[0]/2 
            real_location_y=(100 + (location[0]+ x*(walk_i%self.tick_by_day)/self.tick_by_day) * self.plat + (location[1]+ y*(walk_i%self.tick_by_day)/self.tick_by_day) * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj[1]*(1/2) 
            real_location=[real_location_x,real_location_y]

            
            real_location_x_search=(157 + (location[0]+ x*(walk_i%self.tick_by_day)/self.tick_by_day) * 10 - (location[1]+ y*(walk_i%self.tick_by_day)/self.tick_by_day) * 10-self.offset.x)*self.zoom_scale-vect_list_obj[0]/2 
            real_location_y_search=(97 + (location[0]+ x*(walk_i%self.tick_by_day)/self.tick_by_day) * self.plat + (location[1]+ y*(walk_i%self.tick_by_day)/self.tick_by_day) * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj[1]*(1/2) 
            real_location_search=[real_location_x_search,real_location_y_search]
            

            if obj.action== MANGER :
                obj.image = pygame.image.load(f'data/images/eating/eating{(walk_i%self.tick_by_day)%10+1}.png')
                real_location_x=(148 + (location[0]+ x*(walk_i%self.tick_by_day)/self.tick_by_day) * 10 - (location[1]+ y*(walk_i%self.tick_by_day)/self.tick_by_day) * 10-self.offset.x)*self.zoom_scale-vect_list_obj[0]/2 
                real_location_y=(98 + (location[0]+ x*(walk_i%self.tick_by_day)/self.tick_by_day) * self.plat + (location[1]+ y*(walk_i%self.tick_by_day)/self.tick_by_day) * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj[1]*(1/2) 
                real_location=[real_location_x,real_location_y]
                vect_list_obj[0]*=1.4
                vect_list_obj[1]*=1.4
            
            image_obj=pygame.transform.scale(obj.image, vect_list_obj)

            if -100< real_location [0] and real_location [0] < SCREEN_WIDTH and -100 < real_location [1] and real_location [1] <SCREEN_HEIGHT:

                
                
                # image_red=pygame.transform.scale(image_red, vect_list_obj)

                # image_red.set_alpha(obj.energy)  # Set alpha value based on energy
                if obj.action== CHERCHER_NOURRITURE :
                    searching_image= pygame.image.load(f'data/images/searching/3342_37{walk_i%6}.png')
                    searching_image=pygame.transform.scale(searching_image,vect_list_obj_searching )
                    screen.blit(searching_image, real_location_search)
                
                #pygame.draw.rect(screen, (gbob.), (bar_x, bar_y, bar_width, bar_height))

                screen.blit(image_obj, real_location)
                #screen.blit(image_red, real_location)
            #screen.blit(image_obj, real_location_1)
            
            

            if len(allBobs) != 0:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.show=True
                    self.show_value(mouse_x, mouse_y,real_location_x,real_location_y)
        
    def draw_food(self):
    
        for (x,y) in grille:
            if (grille[(x,y)].qtite_nourriture != 0):
                vect_list_obj_f = [x * self.zoom_scale*0.3 for x in (pygame.Surface.get_width(self.img_appel),pygame.Surface.get_height(self.img_appel))]      
                img_appel=pygame.transform.scale(self.img_appel, vect_list_obj_f)
                real_location_x_f=(150 + (x) * 10 - (y) * 10-self.offset.x)*self.zoom_scale-vect_list_obj_f[0]/2 
                real_location_y_f=(100 + (x) * self.plat + (y) * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj_f[1]*(1/2) 
                real_location_f=[real_location_x_f,real_location_y_f]
                if -100< real_location_f [0] and real_location_f [0] < SCREEN_WIDTH and -100 < real_location_f [1] and real_location_f [1] <SCREEN_HEIGHT:
                    screen.blit(img_appel, real_location_f) 
    

   
    def draw_menu(self):

        image_menu = pygame.image.load('data/images/menu.png')
        image_menu.set_colorkey((0,0,0))
        image_menu = pygame.transform.scale(image_menu, (50, 50))
        screen.blit(image_menu, (SCREEN_WIDTH-170, SCREEN_HEIGHT-100))
   
    def draw_select_load (self,frame=0):
        
        screen.fill((0, 0, 0))
        frame+=1
        
        font = pygame.font.Font(None, 56)

        
        selected_directory = 'saves/'

        files = os.listdir(selected_directory)
        
        move_x=100

        text_positions = []
        j=0
        for i, file in enumerate(files):
            chars_to_remove = [".", "p", "k", "l"]
            for char in chars_to_remove:
                file=file.replace(char, " ")
            text = font.render(file, True, (255, 255, 255))
            if (100+j*60>=460):
                move_x+=200
                j=0
            text_rect = text.get_rect(topleft=(move_x, 100 + j * 60*(SCREEN_HEIGHT/600)))
            j+=1
            text_positions.append((text, text_rect))
            pygame.draw.rect(screen, (169, 169, 169), text_rect, 5)

        text_n = font.render("Your load files, click to select one:", True, (200, 200, 200))
        text_rect_n = text.get_rect(topleft=(100, 30))
    

        selected_file = None

        # 定义颜色
        white = (255, 255, 255)

        # 定义字体和字体大小
        font = pygame.font.Font(None, 36)

        # 定义按钮的大小和位置
        button_width, button_height = 120, 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        load_button_y = SCREEN_HEIGHT // 2 - 30
        delete_button_y = SCREEN_HEIGHT // 2 + 30
        return_button_y = SCREEN_HEIGHT // 2 + 90

        # 定义按钮颜色
        button_color = (100, 100, 100)
        hover_color = (150, 150, 150)

        # 定义按钮标签
        load_text = font.render("Load", True, white)
        delete_text = font.render("Delete", True, white)
        return_text = font.render("Return to menu", True, white)

        image_setting = pygame.image.load('data/images/menu.png')

        image_setting.set_colorkey((0,0,0))

        image_setting = pygame.transform.scale(image_setting, (50, 50))

        image_board = pygame.image.load('data/images/board.png')

        image_board = pygame.transform.scale(image_board, (512,256))

        

            # 游戏循环
        click=False
                    
        

        while True:
            self.draw_background(frame)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not click:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if event.button == 1:  # Left mouse button
                            for text, rect in text_positions:
                                if rect.collidepoint(event.pos):
                                    selected_file = files[text_positions.index((text, rect))]
                                    chars_to_remove = [".", "p", "k", "l"]
                                    for char in chars_to_remove:
                                        selected_file=selected_file.replace(char, "")
                                    print(f"Selected file: {selected_file}")
                                    text_s=selected_file
                                    click=True

                    if SCREEN_WIDTH-170 < mouse_x < SCREEN_WIDTH - 120 and SCREEN_HEIGHT-100 < mouse_y < SCREEN_HEIGHT-50:
                        return 0
                    
                    if click:
                        if button_x <= mouse_x <= button_x + button_width:
                            if load_button_y <= mouse_y <= load_button_y + button_height:
                                print("Load按钮被点击")
                                return text_s
                            elif delete_button_y <= mouse_y <= delete_button_y + button_height:
                                head="saves/"
                                tail=".pkl"
                                file_path_to_delete=head+text_s+tail
                                print(file_path_to_delete)
                                self.delete_file(file_path_to_delete)
                            elif return_button_y <= mouse_y <= return_button_y + button_height:
                                click=False


            
            screen.blit(text_n, text_rect_n)
            screen.blit(image_setting, (SCREEN_WIDTH-170, SCREEN_HEIGHT-100))
            for text, rect in text_positions:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if rect[0] <= mouse_x <= rect[0] + button_width:
                    if rect[1] <= mouse_y <= rect[1] + button_height:
                        pygame.draw.rect(screen, hover_color, (rect[0], rect[1], button_width, button_height))
                screen.blit(text, rect)
            if click:

                # 绘制按钮
                pygame.draw.rect(screen, button_color, (button_x, load_button_y, button_width, button_height))
                pygame.draw.rect(screen, button_color, (button_x, delete_button_y, button_width, button_height))
                pygame.draw.rect(screen, button_color, (button_x, return_button_y, button_width, button_height))

                # 绘制按钮上的文本
                screen.blit(image_board, (SCREEN_WIDTH/2-256, SCREEN_HEIGHT/2-70))
                screen.blit(load_text, (button_x + 20, load_button_y + 10))
                screen.blit(delete_text, (button_x + 10, delete_button_y + 10))
                screen.blit(return_text, (button_x + 10, return_button_y + 10))

                # 检测鼠标悬停
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width:
                    if load_button_y <= mouse_y <= load_button_y + button_height:
                        pygame.draw.rect(screen, hover_color, (button_x, load_button_y, button_width, button_height))
                    elif delete_button_y <= mouse_y <= delete_button_y + button_height:
                        pygame.draw.rect(screen, hover_color, (button_x, delete_button_y, button_width, button_height))
                    elif return_button_y <= mouse_y <= return_button_y + button_height:
                        pygame.draw.rect(screen, hover_color, (button_x, return_button_y, button_width, button_height))

            pygame.display.flip()
    

    def delete_file(self,file_path):
        try:
            os.remove(file_path)
            print(f"The file {file_path} has successfully been deleted.")
        except OSError as e:
            print(f"An error occurred while deleting the file {file_path}: {e}")

    def draw_start(self,frame):

        
        screen.fill((0,0,0))
        # Dessiner l'arrière-plan
        self.draw_background(frame)
        if not self.start_anime :
            

            image_board = pygame.image.load('data/images/board.png')

            image_board = pygame.transform.scale(image_board, (512,256))

            screen.blit(image_board, (SCREEN_WIDTH/2-256, SCREEN_HEIGHT/2-100))

            font = pygame.font.Font(None, 40)
            font2 = pygame.font.Font(None, 20)
            lines = ["START NEW GAME", "LOAD PREVIOUS GAME"]
            deplace = SCREEN_HEIGHT//2
            keys = pygame.key.get_pressed()

            for i, line in enumerate(lines):
                color = (248, 144, 0) if i == int(self.selected_index_start) else (255, 255, 255)
                text = font.render(line, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, deplace + i * 50))
                screen.blit(text, text_rect)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if text_rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
                    self.selected_index_start=i

            notion="select an option (click or 'm'), then press enter"
            text = font2.render(notion, True, (0,0,0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, deplace + 200))
            screen.blit(text, text_rect)

            if keys[pygame.K_m]:
                if self.selected_index_start < 2:
                    self.selected_index_start += 0.4*(self.tick/30)
                else:
                    self.selected_index_start = -1

            # Blit each line onto the text surface with or without highlighting
            # for i, line in enumerate(lines):
            #     text = font.render(line, True, (255, 255, 255))  # Set text color to white
            #     text_rect = text.get_rect(topleft=(2 * SCREEN_WIDTH // 6 + 20, deplace))
            #     screen.blit(text, text_rect.topleft)

            #     # Check if the line is selected, and draw a gray rectangle behind it
            #     if int(self.selected_index_start) == i:
            #         pygame.draw.rect(screen, (169, 169, 169), text_rect, 4)  # Highlight with a gray rectangle
                    
                deplace += 30  # Move to the next line
            # screen.blit(text, text_rect)
            
            if int(self.selected_index_start) == 0:
                if keys[pygame.K_RETURN]:
                    
                    ajouterNourritureGrille()
                    
                    for i in range(numberBob):
                        x,y = randint(0,N-1),randint(0,M-1)
                        b = Bob(bobMemory = 3, bobPerception=5, coord = (x,y))
                        b.coordinates = (x,y)
                        allBobs.append(b)
                        # grille[(x,y)].bobs.append(b)

                    for bob in allBobs:
                        g.all_gameobject.add(BOB_GameObject(bob))

                    self.start_anime = True
                
            if int(self.selected_index_start) == 1:
                if keys[pygame.K_RETURN]:
                    
                    nom_sauvegarde = self.draw_select_load()
                    if not(nom_sauvegarde == 0):
                        for i in range(numberBob-1):
                            x,y = randint(0,N-1),randint(0,M-1)
                            b = Bob(bobMemory = 3, bobPerception=5, coord = (x,y))
                            b.coordinates = (x,y)
                            allBobs.append(b)
                        for bob in allBobs:
                            g.all_gameobject.add(BOB_GameObject(bob))
                        self.charger_jeu(nom_sauvegarde)
                        self.start_anime = True
                    
            
            self.draw_setting()
            

        else:
            # Contrôle du clavier pour déplacer l'écran
            self.keyboard_control()
            # Contrôle du clavier pour effectuer un zoom
            self.zoom_keyboard_control()
            # Dessiner le soleil
            self.draw_sun()
            #self.draw_Floating_Island_Cliff()
            self.draw_cases()
            self.draw_skip()
            for obj in self.all_gameobject:
                # Dessiner l'île flottante
                
                location=()
                location=obj.gbob.previousCoordinates
                # Dessiner des éléments
                
                vect_list_obj_f=()
                real_location_f=()                
                image_fulling = pygame.image.load(f'data/images/fulling/fulling{frame%25+1}.png')
                vect_list_obj_f = [x * self.zoom_scale*obj.taille*0.7 for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]
                image_fulling=pygame.transform.scale(image_fulling, vect_list_obj_f)
                real_location_x=(150 + (location[0]) * 10 - (location[1]) * 10-self.offset.x)*self.zoom_scale-vect_list_obj_f[0]/2
                if (-260+frame) < -10: 
                    real_location_y=(100 + (location[0]) * self.plat + (location[1]) * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj_f[1]*(1/2) -260+frame
                else:
                    real_location_y=(100 + (location[0]) * self.plat + (location[1]) * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj_f[1]*(1/2)-10
                    self.game_running= True
                real_location_f=[real_location_x,real_location_y]
                
                if -100<  real_location_f [0] and  real_location_f [0] < SCREEN_WIDTH and -100 <  real_location_f [1] and  real_location_f [1] <SCREEN_HEIGHT:
                    screen.blit(image_fulling, real_location_f)
                




        pygame.display.flip()
    
    
   
    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_rect.x += self.keyboard_speed
            self.change=True
        if keys[pygame.K_RIGHT]:
            self.camera_rect.x -= self.keyboard_speed
            self.change=True
        if keys[pygame.K_UP]:
            self.camera_rect.y += self.keyboard_speed
            self.change=True
        if keys[pygame.K_DOWN]:
            self.camera_rect.y -= self.keyboard_speed
            self.change=True

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def zoom_keyboard_control(self):
        
        keys = pygame.key.get_pressed()
        if self.zoom_scale <= 10 :
            if keys[pygame.K_c]:
                self.zoom_scale += 0.1
                self.change=True
        if self.zoom_scale >= 0.5 :
            if keys[pygame.K_x]:
                self.zoom_scale -= 0.1
                self.change=True
    
    def tilt_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if self.plat <= 7 :
            if keys[pygame.K_w]:
                self.change=True
                self.plat += 0.1
                self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * self.plat + y *self.plat] for x in range(N) for y in range(N)]
        if self.plat >= 2 :
            if keys[pygame.K_s]:
                self.change=True
                self.plat -= 0.1
                self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * self.plat + y *self.plat] for x in range(N) for y in range(N)]
    
    def demander_nom_sauvegarde(self):
        pygame.font.init()
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(300, 200, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''

        white = (255, 255, 255)

        # 定义字体和字体大小
        font = pygame.font.Font(None, 36)

        # 定义按钮的大小和位置
        button_width, button_height = 120, 50
        button_x = input_box.x + 100
        return_button_y = input_box.y + 100

        # 定义按钮颜色
        hover_color = (150, 150, 150)

        return_text = font.render("Cancel", True, white)


        while True:
            
            for event in pygame.event.get():
                image_broad = pygame.image.load('data/images/broad.png')
                image_broad = pygame.transform.scale(image_broad, (400,200))
                screen.blit(image_broad, (input_box.x - 30, input_box.y - 30))
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    
                    elif return_button_y <= mouse_y <= return_button_y + button_height:
                        return 0
                    
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                            print(f"Text after BACKSPACE: {text}")
                        elif event.key == pygame.K_ESCAPE:
                            text = ''  # Effacer tout le texte en cas d'appui sur la touche Escape
                        else:
                            text += event.unicode

                        # if event.key == pygame.K_F11:
                        #     self.fullscreen = not self.fullscreen
                        #     if self.fullscreen:
                        #         SCREEN_WIDTH=SCREEN_WIDTH_FULL
                        #         SCREEN_HEIGHT=SCREEN_HEIGHT_FULL
                        #         screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                        #     else:
                        #         SCREEN_WIDTH=800
                        #         SCREEN_HEIGHT=600
                        #         screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    
                        
                

            # 检测鼠标悬停
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and return_button_y <= mouse_y <= return_button_y + button_height:
                        pygame.draw.rect(screen, hover_color, (button_x, return_button_y, button_width, button_height))
                    

            width = 200
            

            font1 = pygame.font.Font(None, 20)
            text_show = font1.render("Name of your file (max 10 char.),press enter for confirm", True, (255,255,255))
            screen.blit(text_show, (300 , 200 + 40))

            pygame.draw.rect(screen, color, input_box, 2)
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            screen.blit(return_text, (button_x + 10, return_button_y + 10))
            pygame.display.flip()


    
    
        
    def sauvegarder_jeu(self,nom_sauvegarde):
        
        save_path = os.path.join('saves', f'{nom_sauvegarde}.pkl')

        # Ajoutez les coordonnées initiales des bobs à la liste initial_bob_positions
        initial_bob_positions = [bob.coordinates for bob in allBobs]

        save_data = {
            'tick_by_day': self.tick_by_day,
            'foodE': foodE,
            # 'SCREEN_WIDTH': SCREEN_WIDTH,
            # 'SCREEN_HEIGHT': SCREEN_HEIGHT,
            'N': N,
            'num_bobs': len(allBobs),  # Enregistrez le nombre total de bobs
            'initial_bob_positions': initial_bob_positions,  # Enregistrez uniquement les coordonnées initiales
            # Ajoutez d'autres données à sauvegarder selon vos besoins
        }

        with open(save_path, 'wb') as save_file:
            pickle.dump(save_data, save_file)


    def charger_jeu(self, nom_sauvegarde):
        global SCREEN_WIDTH, SCREEN_HEIGHT, allBobs

        load_path = os.path.join('saves', f'{nom_sauvegarde}.pkl')

        with open(load_path, 'rb') as load_file:
            load_data = pickle.load(load_file)

            # Restaurer les données du jeu depuis le fichier
            self.tick_by_day = load_data['tick_by_day']
            global foodE
            foodE = load_data['foodE']
            # SCREEN_WIDTH = load_data['SCREEN_WIDTH']
            # SCREEN_HEIGHT = load_data['SCREEN_HEIGHT']
            global N
            N = load_data['N']

            # Réinitialiser les coordonnées des bobs existants
            initial_bob_positions = load_data['initial_bob_positions']
            for bob, position in zip(allBobs, initial_bob_positions):
                bob.coordinates = position
    
        

        
class BOB_GameObject(pygame.sprite.Sprite,Bob):
    def __init__(self,Bob):
        super().__init__()
        self.action=Bob.previousAction
        # print(Bob.previousAction)
        self.energy=Bob.energy
        if Bob.energy <= 600:
            self.taille=abs(Bob.energy/800+0.2)
        self.gbob=Bob
        #self.sprites = []
        #self.sprites.append(pygame.image.load('data/images/0.png').convert())
        #self.sprites.append(pygame.image.load('data/images/1.png').convert())
        #self.sprites.append(pygame.image.load('data/images/2.png').convert())
        #self.sprites.append(pygame.image.load('data/images/3.png').convert())
        self.current_sprite = 0
        self.image = pygame.Surface((50, 50))
        #self.image = pygame.image.load('data/images/kirby1.png')
        self.rect = self.image.get_rect()
        self.rect.center = Bob.coordinates
        #self.sprites = [pygame.image.load(f'data/images/kirby1.{i}.png').convert() for i in range(9)]  

        self.current_sprite = 0
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
    


# def read_config_file(filename):
#     config = {}
#     with open(filename, 'r') as file:
#         for line in file:
#             line = line.strip()
#             if line and not line.startswith('#'):
#                 key, value = line.split('=')
#                 config[key.strip()] = eval(value.strip())  # 使用 eval 将字符串转换为相应的类型
#     return config



g=Game()

for i in range(N*M) : g.random_case.append(randint(0,100))






# bob_ex = Bob( bobEnergy=bobMaxE, coord = (0,0))
# allBobs.append(bob_ex)




running = True

frame_count = 0
frame_count_start=0

save_option_shown = False
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                g.is_paused = not g.is_paused
            elif event.key == pygame.K_b:
                g.showbroad = not g.showbroad
            elif event.key == pygame.K_F11:  
                g.fullscreen = not g.fullscreen
                if g.fullscreen:
                    SCREEN_WIDTH=SCREEN_WIDTH_FULL
                    SCREEN_HEIGHT=SCREEN_HEIGHT_FULL
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    SCREEN_WIDTH=800
                    SCREEN_HEIGHT=600
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            elif event.key == pygame.K_o:
                nom_sauvegarde = g.demander_nom_sauvegarde()
                if not(nom_sauvegarde == 0):
                    g.sauvegarder_jeu(nom_sauvegarde)
   
            elif event.key == pygame.K_l:
                nom_sauvegarde = g.draw_select_load ()
                if not(nom_sauvegarde == 0):
                    g.charger_jeu(nom_sauvegarde)



        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                g.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if g.dragging:
                g.image_broad_rect.x = event.pos[0] + g.dragging_offset_x
                g.image_broad_rect.y = event.pos[1] + g.dragging_offset_y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if g.action_button.is_over(pygame.mouse.get_pos()):
                # Lancer un nouveau script Python et quitter le jeu actuel
                subprocess.Popen([sys.executable, "maintesttapha.py"])
                pygame.quit()
                sys.exit()
                print("hey")  # Ce message ne sera pas affiché car le script se termine juste avant

            elif g.image_broad_rect.collidepoint(event.pos):
                g.dragging = True
                g.dragging_offset_x, g.dragging_offset_y = g.image_broad_rect.x - event.pos[0], g.image_broad_rect.y - event.pos[1]
            elif event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if SCREEN_WIDTH-125 < mouse_x < SCREEN_WIDTH-75 and 50 < mouse_y < 100:
                    g.guid = not g.guid
                    if not g.is_paused : 
                        g.is_paused = not g.is_paused
                if SCREEN_WIDTH-195 < mouse_x < SCREEN_WIDTH-145 and 50 < mouse_y < 100:
                    if len (allBobs) == 0:
                        g.all_gameobject.empty()
                        for bob in allBobs:
                            bob.mourir()
                        for i in range(N-1):
                            allBobs.append(Bob(coord = (randint(0,N-1),randint(0,N-1))))
                        for bob in allBobs:
                            g.all_gameobject.add(BOB_GameObject(bob))
                        frame_count = 0
                        frame_count_start=0
                        g.game_running=False
                        g.start_anime= True
                if g.start_anime :
                    if SCREEN_WIDTH -125 < mouse_x < SCREEN_WIDTH - 75 and 50 < mouse_y < 100:
                        frame_count_start+=30

                if SCREEN_WIDTH-100 < mouse_x < SCREEN_WIDTH - 50 and SCREEN_HEIGHT-100 < mouse_y < SCREEN_HEIGHT-50:
                    #g.setting_frame = 0
                    g.selected_index=-1
                    g.setting = not g.setting
                
                if SCREEN_WIDTH-170 < mouse_x < SCREEN_WIDTH - 120 and SCREEN_HEIGHT-100 < mouse_y < SCREEN_HEIGHT-50:
                    key_to_modify="Relancer"
                    new_value=True
                    with open("parametre.py", 'r') as file:
                        lines = file.readlines()

                    with open("parametre.py", 'w') as file:
                        for line in lines:
                            if line.startswith(key_to_modify):
                                line = f"{key_to_modify} = {new_value}\n"
                            file.write(line)
                            
                    pygame.quit()
                    sys.exit()
                    #subprocess.run(["C:/Users/Administrator/AppData/Local/Programs/Python/Python311/python.exe", "d:/python/GameOfLife/configurationpartie.py"])
                    #
                    #config_data = read_config_file("parametre.py")
                    # N=config_data.get("N")
                    # M=config_data.get("M")
                    # g.all_gameobject.empty()
                    # g.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(M)]
                    # for bob in allBobs:
                    #     bob.mourir()
                    # for i in range(N-1):
                    #     allBobs.append(Bob(coord = (randint(0,N-1),randint(0,N-1))))
                    # for bob in allBobs:
                    #     g.all_gameobject.add(BOB_GameObject(bob))
                    
                    
                                
            if int(g.selected_index) ==0:
                    if event.button == 4:  # Mouse wheel scroll up
                                    # Increase value of the selected line
                        g.tick_by_day += 1  # Adjust this line based on your specific use case
                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        g.tick_by_day -= 1  # Adjust this line based on your specific use case
            
            if int(g.selected_index) ==2:
                    if event.button == 4:  # Mouse wheel scroll up
                                    # Increase value of the selected line
                        SCREEN_WIDTH += 5  # Adjust this line based on your specific use case
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        SCREEN_WIDTH -= 5  # Adjust this line based on your specific use case
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            if int(g.selected_index) ==3:
                    if event.button == 4:  # Mouse wheel scroll up
                                    # Increase value of the selected line
                        SCREEN_HEIGHT += 5  # Adjust this line based on your specific use case
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        SCREEN_HEIGHT -= 5  # Adjust this line based on your specific use case
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            if int(g.selected_index) ==4:
                    if event.button == 4:  # Mouse wheel scroll up
                                    # Increase value of the selected line
                        N+=1   # Adjust this line based on your specific use case
                        g.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(M)]
                        # for co in grille:
                        #     co.supprimer()

                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        N-=1  # Adjust this line based on your specific use case
                        g.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(M)]
                        # for co in grille:
                        #     co.supprimer()
                        # grille=g.list_x_y

            if int(g.selected_index) ==5:
                    if event.button == 4:  # Mouse wheel scroll up
                                    # Increase value of the selected line
                        g.costum=(g.costum+1)%8

                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        g.costum=(g.costum-1)%8
            
            if int(g.selected_index) ==6:
                    if event.button == 4:  # Mouse wheel scroll up
                                    # Increase value of the selected line
                        g.costum_case=(g.costum_case+1)%6
                        g.change=True

                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        g.costum_case=(g.costum_case-1)%6
                        g.change=True
                

    if g.game_running:
        g.draw(frame_count)

        

            

        if  not g.is_paused:
            cProfile.run('g.draw(frame_count)')
            frame_count += 1
            if frame_count % g.tick_by_day == 0:
                if g.sombre == 200:
                    g.day_night=1

                if g.sombre == 50:
                    g.day_night=0

                if not g.day_night:
                    g.sombre += 1
                else:
                    g.sombre -= 1

                if (frame_count%100==0):
                    renouvellerNourriture()
                for b in allBobs:
                    if(not b.dejaJoue() and not b.seProteger() and not b.reproductionSexuee() and not b.reproduction() and not b.manger()):
                        b.bobDeplacement()
                    
                    

                g.all_gameobject.empty()

                

                for bob in allBobs:
                    g.all_gameobject.add(BOB_GameObject(bob))


                    for j in g.all_gameobject:
                        j.update_position()
                
            # for j in g.all_gameobject:
            #     j.update_animation(frame_count)
                        
            



    else:
        if g.start_anime:
            frame_count_start += 1

        g.draw_start(frame_count_start)
        
        

        

        

    
    clock.tick(g.tick)
    
pygame.quit()