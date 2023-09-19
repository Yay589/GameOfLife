import pygame
import sys
import random
from Objet import BOB
from Objet import Nourriture
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('BOB LAND')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self):
        global gameTick
        gameTick = 0
        Nourriture_group = pygame.sprite.Group()
        bob_group = pygame.sprite.Group()
        # Create 5 instances of BOB and add them to the group
        for bob in range(5):
            new_bob = BOB(random.randrange(0, SCREEN_WIDTH-5),
                          random.randrange(0, SCREEN_HEIGHT-5))
            bob_group.add(new_bob)

        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, 2000)  # one spawn evry 2 seconds

        while True:

            for event in pygame.event.get():  # pygame.event.get() return all the envents, like SPAWN_EVENT
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == SPAWN_EVENT:
                    new_Nourriture = Nourriture(random.randrange(
                        0, SCREEN_WIDTH-5), random.randrange(0, SCREEN_HEIGHT-5))
                    Nourriture_group.add(new_Nourriture)

            pygame.display.flip()
            # If a bob enters into collision with the food, the food will be removed as if the bob had eaten it.
            for bobs in bob_group:
                for nurri in Nourriture_group:
                    if pygame.sprite.collide_rect(bobs, nurri):
                        Nourriture_group.remove(nurri)

            # all bobs have too contently move
            for bob in range(5):
                BOB.bouger(bob_group.sprites()[bob])

            # the background color in rgb notation.
            self.screen.fill((0, 0, 0))
            bob_group.draw(self.screen)  # drow bobs and food  in the screen.
            # Update the screen to view the next frame of Bob's animation..
            bob_group.update()
            Nourriture_group.draw(self.screen)
            self.clock.tick(20)

            """
            gameTick += 1
            speed = 500
            # The number chosen is arbitrary and should be variable for the user
            day = gameTick//speed
            hours = int(((gameTick/speed) % 1.0)*24)  # curent hour
            minutes = int(((((gameTick/speed) % 1.0)*24) % 1.0)*60)
            if (gameTick % (speed//10) == 0):
                # Print the current time in the terminal for visualisation
                print(f"Day number {day}, {hours}h:{minutes}min\n")
            """


if __name__ == '__main__':
    game = Game()
    game.run()
