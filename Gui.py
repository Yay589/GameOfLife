from parametre import *
from nourriture import *
from Sprite import *
from Render import *
from random import *
import pygame

pygame.init()
pygame.font.init()


g=Render()

ajouterNourritureGrille()

for i in range(N-1):
    x,y = randint(0,N-1),randint(0,N-1)
    b = Bob(bobMemory = 3, coord = (x,y))
    b.coordinates = (x,y)
    allBobs.append(b)
    grille[(x,y)].bobs.append(b)

for bob in allBobs:
    g.all_gameobject.add(BobSprite(bob))




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
                    SCREEN_HEIGHT=SCREEN_HEIGHT_FULL
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
                            g.all_gameobject.add(BobSprite(bob))
                        frame_count = 0
                        frame_count_start=0
                        g.game_running=False
                        g.start_anime= True
                if g.start_anime :
                    if SCREEN_WIDTH -125 < mouse_x < SCREEN_WIDTH - 75 and 50 < mouse_y < 100:
                        frame_count_start+=30

                if SCREEN_WIDTH-100 < mouse_x < SCREEN_WIDTH - 50 and SCREEN_HEIGHT-100 < mouse_y < SCREEN_HEIGHT-50:
                    g.setting_frame = 0
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
            if frame_count % 15 == 0:
                if g.sombre == 200:
                    g.day_night=1

                if g.sombre == 50:
                    g.day_night=0

                if not g.day_night:
                    g.sombre += 1
                else:
                    g.sombre -= 1

                #allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(N*2)]
                for b in allBobs:
                    if(not b.reproduction()):
                        if(not b.manger()):
                            b.bobDeplacement()

                g.all_gameobject.empty()

                

                for bob in allBobs:
                    g.all_gameobject.add(BobSprite(bob))


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