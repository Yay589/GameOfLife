import pygame
import time
import sys
import random
from Object import *
from Render import *
from World  import *

class Game:

    def __init__(self):

        # Demander à l'utilisateur de saisir deux valeurs séparées par un espace
        dimensions_input = input("Quelle dimension (N x M) de la carte souhaitez-vous ? Entrez N M : ")

        # Diviser les valeurs saisies en une liste en utilisant l'espace comme séparateur
        dimensions_list = dimensions_input.split()

        # Assurez-vous que deux valeurs ont été saisies
        while len(dimensions_list) != 2:
            print("Veuillez saisir exactement deux valeurs séparées d'un espace.")
            dimensions_input = input("Quelle dimension (N x M) de la carte souhaitez-vous ? Entrez N M : ")
            dimensions_list = dimensions_input.split()
        
        self.n, self.m = map(int, dimensions_list)
        self.r = Render(self.n, self.m)
            
        self.nombre_de_bob = int(input("Combien de bobs voudriez-vous simuler ? : "))
        self.nombre_de_nourriture = int(input("Combien de nourriture voudriez-vous ajouter au départ de la simulation ? : "))

        listObjects = []

        for i in range(self.nombre_de_bob):
            listObjects.append(BOB(i))
        for i in range(self.nombre_de_bob, self.nombre_de_nourriture+self.nombre_de_bob):
            listObjects.append(Nourriture(i))

        for i in listObjects:
            self.r.world.addOnMap(i)
        
        running = True
        clock = pygame.time.Clock()
        
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.r.draw()
            for i in listObjects:
                self.r.world.move(i)
            """ 
            for k,v in self.r.world.world.items():
                current_cursor = 0
                while len(v) > 1: #si la liste comptien plus d'un objet (bob ou nourriture) c'est qu'il y a colision et donc conflit.
                    if v[current_cursor].type == v[current_cursor+1].type and v[current_cursor].alive == v[current_cursor+1].alive == True:
                        if v[current_cursor].energy < v[current_cursor+1].energy:
                            v[current_cursor+1].energy+= v[current_cursor].energy
                            v[current_cursor].alive = False
                            self.r.world.world[k].remove(v[current_cursor])
                            
                        elif v[current_cursor].energy > v[current_cursor+1].energy:
                            v[current_cursor].energy+= v[current_cursor+1].energy
                            v[current_cursor+1].alive = False
                            self.r.world.world[k].remove(v[current_cursor+1])
                        else:
                            v[current_cursor].alive = False
                    elif v[current_cursor].aviable == v[current_cursor+1].aviable == True:
                        bob = v[current_cursor] if isinstance(v[current_cursor],BOB) else v[current_cursor+1]
                        food = v[current_cursor] if isinstance(v[current_cursor],Nourriture) else v[current_cursor+1]
                        bob.energy +=  food.energy                    
                        self.r.world.world[k].remove(v[current_cursor] if isinstance(v[current_cursor],Nourriture) else v[current_cursor+1])
                        
                    current_cursor+= 1
                
                
            # notes pour moi : pourquoi world est vide ?
            for i in self.r.world.world.values():
                print(i)
                self.r.world.move(i)
            """
            
            clock.tick(20)
            
        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()
