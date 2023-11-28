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
allFoods = [Nourriture(coord = (randint(0,N-1),randint(0,N-1))) for i in range(2*N)]


for bob in allBobs:
    g.all_gameobject.add(BobSprite(bob))

for food in allFoods:
    g.all_gameobject.add(FoodSprite(food))


bob_ex = Bob( bobEnergy=bobMaxE, coord = (0,0))
allBobs.append(bob_ex)

food_ex = Nourriture()
allFoods.append(food_ex)

running = True
is_paused = False


save_option_shown = False
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_paused = not is_paused

    
    g.draw(is_paused)    
    

    if not is_paused:
        


        for b in allBobs:
            if(not b.reproduction()):
                if(not b.manger()):
                    b.bouger()

        g.all_gameobject.empty()

        for bob in allBobs:
            g.all_gameobject.add(BobSprite(bob))
            for j in g.all_gameobject:
                j.update_position()
                
        for food in allFoods:
            g.all_gameobject.add(FoodSprite(food))
        
        
    
    clock.tick(15)
    
pygame.quit()