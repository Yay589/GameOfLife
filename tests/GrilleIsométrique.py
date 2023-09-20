import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Grille Isométrique")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Taille de la grille
n, m = 10, 10

# Taille d'une tuile isométrique
largeur_tuile = 60
hauteur_tuile = 30

# Fonction pour dessiner une tuile isométrique


def dessiner_tuile(x, y, couleur):
    points = [(x, y + hauteur_tuile), (x + largeur_tuile, y),
              (x + 2 * largeur_tuile, y + hauteur_tuile), (x + largeur_tuile, y + 2 * hauteur_tuile)]
    pygame.draw.polygon(fenetre, couleur, points)
    # Dessiner un contour autour de la tuile
    pygame.draw.lines(fenetre, NOIR, True, points, 1)


# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill(BLANC)

    # Dessiner la grille isométrique
    for i in range(n):
        for j in range(m):
            x = i * 2 * largeur_tuile
            y = j * 2 * hauteur_tuile
            if (i + j) % 2 == 0:
                couleur = NOIR
            else:
                couleur = BLANC
            dessiner_tuile(x, y, couleur)

    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
