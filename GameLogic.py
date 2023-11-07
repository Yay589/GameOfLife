from random import *
from parametre import *
from math import trunc
from nourriture import Nourriture
from case import Case
from bob import Bob


if __name__ == '__main__':
    #game = Game()
    #game.run()

    bob1 = Bob()
    bob2 = Bob(BobEnergy=150,coord=[0,100])
    bob3 = Bob()

    for i in range(10):
        bob2.speak()
        bob2.bouger()

    food1 = Nourriture()
    food1.speak()
    bob2.manger(food1)
    bob2.speak()
    food1.speak()