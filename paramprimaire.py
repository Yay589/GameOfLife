import pygame
import sys
import os

# Charger les valeurs par défaut depuis le fichier parametre.py
param_file_path = "parametre.py"

with open(param_file_path, "r") as param_file:
    lines = param_file.readlines()

for line in lines:
    if line.strip().startswith(("graphicalInterfaceON", "soloReproductionON", "duoReproductionON",
                                "speedON", "massON", "perceptionON", "memoryON")):
        variable_name, value = line.split("=")
        globals()[variable_name.strip()] = value.strip() == "True"

# Initialiser Pygame
pygame.init()

# Définir la taille de la fenêtre
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Activer/Desactiver des fonctionnalités primaires")

# Ajouter le chemin de votre image d'arrière-plan
background_image_path = os.path.join("data", "images", "background.jpg")

# Charger l'image d'arrière-plan
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, window_size)  # Redimensionner l'image
background_rect = background_image.get_rect()

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
button_on_color = (0, 255, 0)  # Vert
button_off_color = (255, 0, 0)  # Rouge
default_confirm_color = (100, 100, 100)  # Couleur des boutons "Default" et "Confirmer"

# Police
font = pygame.font.Font("font/Gumela.ttf", 24)

# Fonction pour mettre à jour les valeurs dans le fichier parametre.py
def update_param_file():
    with open(param_file_path, "r") as param_file:
        lines = param_file.readlines()

    with open(param_file_path, "w") as param_file:
        for line in lines:
            if line.strip().startswith(("graphicalInterfaceON", "soloReproductionON", "duoReproductionON",
                                        "speedON", "massON", "perceptionON", "memoryON")):
                variable_name, _ = line.split("=")
                new_value = "True" if variable_name.strip() in active_buttons else "False"
                line = f"{variable_name}= {new_value}\n"
            param_file.write(line)

# Boutons
button_positions = {
    "graphicalInterfaceON": (window_size[0] // 4, window_size[1] // 2 - 100),
    "soloReproductionON": (window_size[0] // 4, window_size[1] // 2 - 50),
    "duoReproductionON": (window_size[0] // 4, window_size[1] // 2),
    "speedON": (window_size[0] // 4, window_size[1] // 2 + 50),
    "massON": (3 * window_size[0] // 4, window_size[1] // 2 - 100),
    "perceptionON": (3 * window_size[0] // 4, window_size[1] // 2 - 50),
    "memoryON": (3 * window_size[0] // 4, window_size[1] // 2),
    "default": (window_size[0] // 4, window_size[1] // 2 + 100),
    "confirm": (3 * window_size[0] // 4, window_size[1] // 2 + 100),
}

active_buttons = set()

# Boucle principale
while True:
    # Charger les valeurs depuis le fichier parametre.py au lancement
    if not active_buttons:
        with open(param_file_path, "r") as param_file:
            lines = param_file.readlines()

        for line in lines:
            if line.strip().startswith(("graphicalInterfaceON", "soloReproductionON", "duoReproductionON",
                                        "speedON", "massON", "perceptionON", "memoryON")):
                variable_name, value = line.split("=")
                if value.strip() == "True":
                    active_buttons.add(variable_name.strip())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gestion des événements de la souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button, position in button_positions.items():
                rect = pygame.Rect(position[0], position[1], 100, 30)
                if rect.collidepoint(event.pos):
                    if button == "default":
                        active_buttons = set(button_positions.keys()) - {"default"}
                    elif button == "confirm":
                        update_param_file()
                        pygame.quit()
                        sys.exit()
                    elif button in active_buttons:
                        active_buttons.remove(button)
                    else:
                        active_buttons.add(button)

    # Dessiner l'arrière-plan
    screen.blit(background_image, background_rect)

    # Dessiner les boutons
    for button, position in button_positions.items():
        rect = pygame.Rect(position[0], position[1], 100, 30)
        color = button_on_color if button in active_buttons else button_off_color
        if button == "default" or button == "confirm":
            color = default_confirm_color
        pygame.draw.rect(screen, color, rect)

        # Dessiner le texte ON/OFF au centre du bouton
        if button != "default" and button != "confirm":
            button_text = font.render("ON" if button in active_buttons else "OFF", True, white)
            text_rect = button_text.get_rect(center=rect.center)
            screen.blit(button_text, text_rect)

            # Dessiner le texte du paramètre au-dessus du bouton
            parameter_text = font.render(button, True, black)
            text_rect = parameter_text.get_rect(center=(rect.center[0], rect.top - 10))
            screen.blit(parameter_text, text_rect)
        elif button == "default":
            default_text = font.render("Default", True, white)
            text_rect = default_text.get_rect(center=rect.center)
            screen.blit(default_text, text_rect)
        elif button == "confirm":
            confirm_text = font.render("Confirmer", True, white)
            text_rect = confirm_text.get_rect(center=rect.center)
            screen.blit(confirm_text, text_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()
