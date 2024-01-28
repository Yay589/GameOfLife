from parametre import *
from Sprite import *
from Render import *
from random import *
import pygame

pygame.init()
pygame.font.init()


g=Render()
print(g.list_x_y)


for i in range(N-1):
        allBobs.append(Bob(coord = (randint(0,N-1),randint(0,N-1))))


for bob in allBobs:
    g.all_gameobject.add(BobSprite(bob))


bob_ex = Bob( bobEnergy=bobMaxE, coord = (0,0))
allBobs.append(bob_ex)

running = True

save_option_shown = False
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                g.is_paused = not g.is_paused
    

    if g.game_running:
        
        g.draw()    

        if  not g.is_paused:
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
                        b.bouger()

            g.all_gameobject.empty()

            for bob in allBobs:
                g.all_gameobject.add(BobSprite(bob))


                for j in g.all_gameobject:
                    j.update_position()

    else:
        g.draw_start()
    
    clock.tick(15)
    
pygame.quit()
