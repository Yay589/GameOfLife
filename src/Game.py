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
            
            clock.tick(20)
            
        pygame.quit()



if __name__ == '__main__':
    game = Game()
    game.run()
