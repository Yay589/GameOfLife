import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définition de la taille de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Grille Losange")

# Couleurs
BLANC = (0, 100, 0)
NOIR = (34, 139, 34)

# Taille de la grille
n, m = 10, 10

# Taille d'une tuile losange
largeur_tuile = 60
hauteur_tuile = 30

# Coordonnées de la caméra
camera_x = -(largeur//2)+largeur_tuile
camera_y = 0


# Fonction pour dessiner une tuile losange


def dessiner_tuile(x, y, couleur):
    points = [(x, y + hauteur_tuile), (x + largeur_tuile, y),
              (x + 2 * largeur_tuile, y + hauteur_tuile), (x + largeur_tuile, y + 2 * hauteur_tuile)]
    pygame.draw.polygon(fenetre, couleur, points)
    # Dessiner un contour autour de la tuile
    pygame.draw.lines(fenetre, NOIR, True, points, 1)

# Fonction pour déplacer la caméra


def deplacer_camera(dx, dy):
    global camera_x, camera_y
    camera_x += dx
    camera_y += dy


# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                deplacer_camera(-10, 0)  # Déplacer la caméra vers la gauche
            elif event.key == pygame.K_RIGHT:
                deplacer_camera(10, 0)  # Déplacer la caméra vers la droite
            elif event.key == pygame.K_UP:
                deplacer_camera(0, -10)  # Déplacer la caméra vers le haut
            elif event.key == pygame.K_DOWN:
                deplacer_camera(0, 10)  # Déplacer la caméra vers le bas

    fenetre.fill((255, 255, 255))

    # Dessiner la grille losange
    for i in range(n):
        for j in range(m):
            x = (i - j) * largeur_tuile - camera_x
            y = (i + j) * hauteur_tuile - camera_y
            if (i + j) % 2 == 0:
                couleur = NOIR
            else:
                couleur = BLANC
            dessiner_tuile(x, y, couleur)

    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()
