import curses
import pickle
from random import *
from parametre import *
from math import trunc
from nourriture import *
from case import Case
from bob import Bob
from affichage import *

#fonction pour avoir des infos globales sur notre grille
def avgSpeed():
    i = 0
    speedSum = 0
    for c in grille:
        for b in grille[c].bobs :
            speedSum += b.speed
            i += 1
    if(i==0):
        print("Tout les bobs sont morts")
        return(-1)
    else:
        return speedSum/i

def nbBobs():
    i = 0
    for c in grille:
        for b in grille[c].bobs :
            i += 1
    return i


def show_menu(stdscr):
    # Affiche le menu
    stdscr.addstr(0, 0, "Appuyez sur 'C' pour Continuer le jeu")
    stdscr.addstr(1, 0, "Appuyez sur 'S' pour Sauvegarder")
    stdscr.addstr(2, 0, "Appuyez sur 'Q' pour QUITTER")
    stdscr.refresh()

    # Récupère la touche pressée dans le menu
    key_in_menu = stdscr.getch()

    # Gère les actions dans le menu
    if key_in_menu == ord('c') or key_in_menu == ord('C'):
        return 'continue'
    elif key_in_menu == ord('s') or key_in_menu == ord('S'):
        return 'save'
    elif key_in_menu == ord('q') or key_in_menu == ord('Q'):
        return 'quit'
    else:
        return 'unknown'


if __name__ == '__main__':
    stdscr = curses.initscr()
     # Désactive le curseur par défaut
    curses.curs_set(0)

    while True:
        # Efface l'écran
        
        stdscr.clear()

        # Affiche le jeu
        for i in range(numberBob):
            allBobs.append(Bob(coord=(randint(0, N - 1), randint(0, N - 1))))
        renouvellerNourriture()
        afficheGrilleSimple()

        # Vérifie si la touche Échap est pressée
        if stdscr.getch() == 27:
            action = show_menu(stdscr)
            if action == 'continue':
                continue
            elif action == 'save':
                with open('game_save.pkl', 'wb') as file:
                    pickle.dump((allBobs, grille), file)
                
                stdscr.addstr(1, 0, "Jeu sauvegardé avec succès.")
                break
            elif action == 'quit':
                break  # Quitte complètement le jeu

    curses.endwin()  # Termine l'interface curses




