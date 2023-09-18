
import pygame
import sys
import random
from objet import BOB
from objet import Nourriture

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
fenetre_largeur, fenetre_hauteur = 1280, 720
fenetre = pygame.display.set_mode((fenetre_largeur, fenetre_hauteur))
pygame.display.set_caption("Grille pygame")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Dimensions de la grille
grille_largeur, grille_hauteur = 100, 100
taille_case = fenetre_largeur // grille_largeur

# Position de la grille pour la centrer
decalage_x = (fenetre_largeur - grille_largeur * taille_case) // 2
decalage_y = (fenetre_hauteur - grille_hauteur * taille_case) // 2

# Fonction pour dessiner la grille


def dessiner_grille():
    for x in range(grille_largeur):
        for y in range(grille_hauteur):
            rect = pygame.Rect(x * taille_case + decalage_x, y *
                               taille_case + decalage_y, taille_case, taille_case)
            pygame.draw.rect(fenetre, 'white', rect, 1)


# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill('black')
    dessiner_grille()
    pygame.display.flip()

# Quitter pygame
pygame.quit()
sys.exit()
