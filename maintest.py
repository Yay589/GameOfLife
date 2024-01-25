import pygame
from random import *
import math
from Sprite import *
from parametre import *
from case import Case
from bob import Bob
from affichage import *
pygame.init()


pygame.font.init()

# Define the screen dimensions
SCREEN_WIDTH_FULL, SCREEN_HEIGHT_FULL = pygame.display.Info().current_w, pygame.display.Info().current_h
fullscreen = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('BOB_LAND')

class Game:
    def __init__(self) :
        self.setting_frame=0
        self.selected_index = -1
        self.start_anime=False
        self.tick=30
        self.tick_by_day=15
        self.ball_x=0
        self.ball_y=0
        self.angle=0
        self.day_night=0
        self.sombre=200
        self.plat=5
        self.show = False
        self.dragging = False
        self.guid = False
        self.setting = False
        self.show_energy=0
        self.game_running = False
        self.is_paused = False
        self.showbroad = False
        self.all_gameobject=pygame.sprite.Group()
        self.listObjects = []
        self.linital_position = []
        self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(N)]
        #self.random_values_for_tree = random.sample(self.list_x_y, 6)

        # num_points_to_select = N // 5 + 1
        # available_points = self.list_x_y.copy()
        # self.selected_points = []
        # for _ in range(num_points_to_select):
        #     random_point = random.choice(available_points)
        #     self.selected_points.append(random_point)
        #     available_points.remove(random_point)

        self.img_appel = pygame.image.load('data/images/apple.png').convert()
        self.image = pygame.image.load('data/images/grass.png').convert()
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

    def add_object(self, game_object):
        self.listObjects.append(game_object)


    def draw(self,walk_i):

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
        self.draw_Floating_Island_Cliff()

        # Contrôle du clavier pour incliner
        self.tilt_keyboard_control()

        # Dessiner des éléments
        self.draw_cases()
        self.draw_objects(walk_i)

        self.show_broad()

        self.draw_info()

        self.draw_restart()

        

        
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

            screen.blit(image_pause, (535, 50))
        
        self.draw_setting()

        pygame.display.flip()
    
    def draw_guid(self):

        guid_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        guid_surface.fill((128, 128, 128, 128))
        font = pygame.font.Font(None, 24)
        lines = [
            "Welcome to the guidance interface.",
            "You can navigate Bob Land by using the arrow keys: up, down, left, and right.",
            "Press 'c' to zoom in, and 'x' to zoom out.",
            "Press the space bar to pause the game.",
            "Press 'b' to bring up the information board (you can drag it with the mouse).",
            "Click on a specific Bob to learn more about him;",
            "Click on this icon again to exit the guidance."
        ]

        y_position = SCREEN_HEIGHT // 4  # 设置文本的初始纵坐标

        for line in lines:
            text = font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            guid_surface.blit(text, text_rect)
            y_position += text_rect.height + SCREEN_HEIGHT // 25
        screen.blit(guid_surface, (0, 0))


    def draw_background(self, frame):
        image_ground = pygame.image.load(f'data/images/background/background{frame%41}.png')
        image_ground = pygame.transform.scale(image_ground, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_ground.set_alpha(self.sombre)
        screen.blit(image_ground, (0, 0))
    
    def draw_sun(self):
        image_ball = pygame.image.load('data/images/full.png')
        image_ball = pygame.transform.scale(image_ball, (100, 100))
        ball_rect = image_ball.get_rect()
        if not self.is_paused:
            self.angle += 0.02
            self.ball_x = 400 + 400 * math.cos(self.angle)
            self.ball_y = 250 + 200 * math.sin(self.angle)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.ball_x < mouse_x < self.ball_x + 100 and self.ball_y < mouse_y < self.ball_y + 100:
                image_ball = pygame.image.load('data/images/full1.png')
                image_ball = pygame.transform.scale(image_ball, (100*self.zoom_scale, 100*self.zoom_scale))
                
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
            


    def show_broad(self):

        if self.showbroad :

            screen.blit(self.image_broad, self.image_broad_rect)

            font = pygame.font.Font(None, 20)

            text_show = font.render(f"Bob tu veux : {self.show_energy}", True, (0, 0, 0))

            screen.blit(text_show, self.image_broad_rect.move(15, 15))

            text_render = font.render(f"The number of our residents: {len(allBobs)}", True, (0, 0, 0))

            screen.blit(text_render, self.image_broad_rect.move(15, 45))

    def draw_info(self):        
        if self.guid:

            self.draw_guid()

        image_info = pygame.image.load('data/images/info.png')

        image_info.set_colorkey((255, 255, 255))

        image_info = pygame.transform.scale(image_info, (50, 50))

        screen.blit(image_info, (675, 50))

    def draw_skip(self):        
        
        image_skip = pygame.image.load('data/images/skip.png')

        image_skip = pygame.transform.scale(image_skip, (50, 50))

        screen.blit(image_skip, (SCREEN_WIDTH-125, 50))
        
 


    def draw_restart(self):        

        image_restart = pygame.image.load('data/images/restart.png')

        image_restart.set_colorkey((255, 255, 255))

        image_restart = pygame.transform.scale(image_restart, (50, 50))

        screen.blit(image_restart, (605, 50))
    

    def draw_setting(self):        

        image_setting = pygame.image.load('data/images/setting.png')

        image_setting.set_colorkey((255, 255, 255))

        image_setting = pygame.transform.scale(image_setting, (50, 50))

        screen.blit(image_setting, (SCREEN_WIDTH-100, SCREEN_HEIGHT-100))

        if self.setting :
            if self.setting_frame < 5:
                self.setting_frame+=1
                image_setting_a = pygame.image.load(f'data/images/setting/setting{self.setting_frame}.png')
                image_setting_a = pygame.transform.scale(image_setting_a, (2*SCREEN_WIDTH/3,SCREEN_HEIGHT))
                screen.blit(image_setting_a, (SCREEN_WIDTH/6, 0))
            
            else:
                image_setting_a = pygame.image.load(f'data/images/setting/setting{5}.png')
                image_setting_a = pygame.transform.scale(image_setting_a, (2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT))
                screen.blit(image_setting_a, (SCREEN_WIDTH/6, 0))

                font = pygame.font.Font(None, 24)
                lines = [
                    f"Tick for one day:{self.tick_by_day}",
                    f"Energy for each food:{foodE}",
                    f"SCREEN_WIDTH:{SCREEN_WIDTH}",
                    f"SCREEN_HEIGHT:{SCREEN_HEIGHT}",
                    f"Number of cases:{N}"
                ]

                deplace=80
                
                up = pygame.image.load(f'data/images/setting/up.png')
                up = pygame.transform.scale(up, (50,50))
                screen.blit(up, (SCREEN_WIDTH/6+40, 370))
                
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_n]:
                    if self.selected_index < 5 :
                        self.selected_index += 0.5
                    else:
                        self.selected_index=-1

                # Blit each line onto the text surface with or without highlighting
                for i, line in enumerate(lines):
                    text = font.render(line, True, (255, 255, 255))  # Set text color to white
                    text_rect = text.get_rect(topleft=(2 * SCREEN_WIDTH // 6 + 20, deplace))
                    screen.blit(text, text_rect.topleft)

                    # Check if the line is selected, and draw a gray rectangle behind it
                    if int(self.selected_index) == i:
                        pygame.draw.rect(screen, (169, 169, 169), text_rect, 2)  # Highlight with a gray rectangle
                    
                    deplace += 30  # Move to the next line
            
        
        else:
            if self.setting_frame > 0:
                self.setting_frame-=1
                image_setting_a = pygame.image.load(f'data/images/setting/setting{self.setting_frame}.png')
                image_setting_a = pygame.transform.scale(image_setting_a, (2*SCREEN_WIDTH/3,SCREEN_HEIGHT))
                screen.blit(image_setting_a, (SCREEN_WIDTH/6, 0))
                    


                


    def draw_cases(self):
        for i in self.list_x_y:
            #screen.blit(self.image, i)
            vect_list = [x * self.zoom_scale for x in (self.rect.width ,self.rect.height*(self.plat/5))]
            image=pygame.transform.scale(self.image, vect_list)

            case_locattion=[(i[0]-self.offset.x-self.rect.width/2)*self.zoom_scale
                                ,(i[1]-self.offset.y)* self.zoom_scale]
            if -100< case_locattion [0] and case_locattion [0] < SCREEN_WIDTH and -100 < case_locattion [1] and case_locattion [1] <SCREEN_HEIGHT:   
                screen.blit(image, case_locattion)
    
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
           
            if (obj.gbob.previousCoordinates[1]- obj.gbob.coordinates[1])>0 or (obj.gbob.previousCoordinates[0]- obj.gbob.coordinates[0])<0:
                image_red = pygame.image.load(f'data/images/walking_blue/walking{walk_i%10+1}.png')
                obj.image = pygame.image.load(f'data/images/walking/walking{walk_i%10+1}.png') 
            else:
                image_red = pygame.image.load(f'data/images/walking_blue1/walking{walk_i%10+1}.png')
                obj.image = pygame.image.load(f'data/images/walking1/walking{walk_i%10+1}.png')
            vect_list_obj = [x * self.zoom_scale*obj.taille*0.08 for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]      
            
        
            for case_f in grille:
                if case_f == obj.gbob.previousCoordinates :
                    obj.image = pygame.image.load(f'data/images/eating/eating{(walk_i%self.tick_by_day)%10+1}.png') 

            image_obj=pygame.transform.scale(obj.image, vect_list_obj)
            
            
            real_location_x=(150 + (location[0]+ x*(walk_i%self.tick_by_day)/self.tick_by_day) * 10 - (location[1]+ y*(walk_i%self.tick_by_day)/self.tick_by_day) * 10-self.offset.x)*self.zoom_scale-vect_list_obj[0]/2 
            real_location_y=(100 + (location[0]+ x*(walk_i%self.tick_by_day)/self.tick_by_day) * self.plat + (location[1]+ y*(walk_i%self.tick_by_day)/self.tick_by_day) * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj[1]*(1/2) 
            real_location=[real_location_x,real_location_y]

            
            if -100< real_location [0] and real_location [0] < SCREEN_WIDTH and -100 < real_location [1] and real_location [1] <SCREEN_HEIGHT:

                
                
                image_red=pygame.transform.scale(image_red, vect_list_obj)

                image_red.set_alpha(obj.energy)  # Set alpha value based on energy
                screen.blit(image_obj, real_location)
                screen.blit(image_red, real_location)
            #screen.blit(image_obj, real_location_1)
            
            

        if len(allBobs) != 0:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.show=True
                self.show_value(mouse_x, mouse_y,real_location_x,real_location_y)
        
        
        for (x,y) in grille:
            if (grille[(x,y)].qtite_nourriture != 0):
                vect_list_obj_f = [x * self.zoom_scale*0.5 for x in (pygame.Surface.get_width(self.img_appel),pygame.Surface.get_height(self.img_appel))]      
                img_appel=pygame.transform.scale(self.img_appel, vect_list_obj_f)
                real_location_x_f=(150 + (x) * 10 - (y) * 10-self.offset.x)*self.zoom_scale-vect_list_obj_f[0]/2 
                real_location_y_f=(100 + (x) * self.plat + (y) * self.plat-self.offset.y+self.plat)*self.zoom_scale-vect_list_obj_f[1]*(1/2) 
                real_location_f=[real_location_x_f,real_location_y_f]
                screen.blit(img_appel, real_location_f) 
   
    
    def draw_start(self,frame):

        
        screen.fill((0,0,0))
        # Dessiner l'arrière-plan
        self.draw_background(frame)
        if not self.start_anime :
            button_color = (0, 255, 0)
            button_width, button_height = 200, 50
            button_x, button_y = (SCREEN_WIDTH - button_width) // 2, (SCREEN_HEIGHT - button_height) // 2
            font = pygame.font.Font(None, 36)
            text = font.render("Start Game", True, (0, 0, 0))
            text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
            screen.blit(text, text_rect)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                    self.start_anime = True

        else:
            # Contrôle du clavier pour déplacer l'écran
            self.keyboard_control()
            # Contrôle du clavier pour effectuer un zoom
            self.zoom_keyboard_control()
            # Dessiner le soleil
            self.draw_sun()
            self.draw_Floating_Island_Cliff()
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
                vect_list_obj_f = [x * self.zoom_scale*obj.taille*1.6 for x in (pygame.Surface.get_width(obj.image),pygame.Surface.get_height(obj.image))]
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
        if keys[pygame.K_RIGHT]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_UP]:
            self.camera_rect.y += self.keyboard_speed
        if keys[pygame.K_DOWN]:
            self.camera_rect.y -= self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def zoom_keyboard_control(self):
        
        keys = pygame.key.get_pressed()
        if self.zoom_scale <= 10 :
            if keys[pygame.K_c]:
                self.zoom_scale += 0.1
        if self.zoom_scale >= 0.5 :
            if keys[pygame.K_x]:
                self.zoom_scale -= 0.1
    
    def tilt_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.plat += 0.1
            self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * self.plat + y *self.plat] for x in range(N) for y in range(N)]

        if keys[pygame.K_s]:
            self.plat -= 0.1
            self.list_x_y = [[150 + x * 10 - y * 10, 100 + x * self.plat + y *self.plat] for x in range(N) for y in range(N)]

    def save_game(self):
        with open('src/save.txt', 'w') as file:
            for bob in allBobs:
                for key, value in bob():
                    print(bob.energy)
                    print(value)
                    print("\n")
                    file.write(f"{key},{value}\n")
        
class BOB_GameObject(pygame.sprite.Sprite,Bob):
    def __init__(self,Bob):
        super().__init__()
        self.energy=Bob.energy
        self.taille=Bob.energy/800+0.2
        self.gbob=Bob
        #self.sprites = []
        #self.sprites.append(pygame.image.load('data/images/0.png').convert())
        #self.sprites.append(pygame.image.load('data/images/1.png').convert())
        #self.sprites.append(pygame.image.load('data/images/2.png').convert())
        #self.sprites.append(pygame.image.load('data/images/3.png').convert())
        self.current_sprite = 0
        self.image = pygame.image.load('data/images/kirby.png')
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
    



g=Game()







ajouterNourritureGrille()

for i in range(N-1):
    x,y = randint(0,N-1),randint(0,N-1)
    b = Bob(bobMemory = 3, bobPerception=5, coord = (x,y))
    b.coordinates = (x,y)
    allBobs.append(b)
    # grille[(x,y)].bobs.append(b)

for bob in allBobs:
    g.all_gameobject.add(BOB_GameObject(bob))


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
                fullscreen = not fullscreen
                if fullscreen:
                    SCREEN_WIDTH=SCREEN_WIDTH_FULL
                    SCREEN_HEIGHT=SCREEN_HEIGHT_FULL
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    SCREEN_WIDTH=800
                    SCREEN_HEIGHT=600
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                g.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if g.dragging:
                g.image_broad_rect.x = event.pos[0] + g.dragging_offset_x
                g.image_broad_rect.y = event.pos[1] + g.dragging_offset_y
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if g.image_broad_rect.collidepoint(event.pos):
                g.dragging = True
                g.dragging_offset_x, g.dragging_offset_y = g.image_broad_rect.x - event.pos[0], g.image_broad_rect.y - event.pos[1]
            elif event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 675 < mouse_x < 725 and 50 < mouse_y < 100:
                    g.guid = not g.guid
                    if not g.is_paused : 
                        g.is_paused = not g.is_paused
                if 605 < mouse_x < 655 and 50 < mouse_y < 100:
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
                        SCREEN_WIDTH += 1  # Adjust this line based on your specific use case
                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        SCREEN_WIDTH -= 1  # Adjust this line based on your specific use case
            
            if int(g.selected_index) ==3:
                    if event.button == 4:  # Mouse wheel scroll up
                                    # Increase value of the selected line
                        SCREEN_HEIGHT += 1  # Adjust this line based on your specific use case
                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        SCREEN_HEIGHT -= 1  # Adjust this line based on your specific use case
            if int(g.selected_index) ==4:
                    if event.button == 4:  # Mouse wheel scroll up
                                    # Increase value of the selected line
                        N += 1  # Adjust this line based on your specific use case
                        g.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(N)]
                    elif event.button == 5:  # Mouse wheel scroll down
                                    # Decrease value of the selected line
                        N -= 1  # Adjust this line based on your specific use case
                        g.list_x_y = [[150 + x * 10 - y * 10, 100 + x * 5 + y * 5] for x in range(N) for y in range(N)]
                

    if g.game_running:
        
        g.draw(frame_count)    
        


            

        if  not g.is_paused:

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
                    if(not b.reproduction()):
                        if(not b.manger()):
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