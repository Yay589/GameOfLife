import pygame
import sys

# Charger les valeurs par défaut
N = 100
M = 100
numberBob = 100

# Initialiser Pygame
pygame.init()

# Définir la taille de la fenêtre
window_size = (400, 400)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Configuration de la partie")

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
light_blue = (173, 216, 230)  # Couleur de fond lorsqu'une boîte est active
light_red = (255, 99, 71)  # Couleur de fond pour indiquer une saisie incorrecte

# Police
font = pygame.font.Font("font/Gumela.ttf", 24)

# Fonction pour vérifier si une chaîne est un nombre
def is_number(s):
    return s.isdigit() or (s.startswith('-') and s[1:].isdigit())

# Fonction pour mettre à jour les valeurs dans le fichier parametre.py
def update_param_file():
    param_file_path = "parametre.py"

    with open(param_file_path, "r") as param_file:
        lines = param_file.readlines()

    with open(param_file_path, "w") as param_file:
        for line in lines:
            if line.strip().startswith(("N =", "M =", "numberBob =")):
                variable_name, _ = line.split("=")
                new_value = next((box['text'] for box in input_boxes if box['label'] == "Longeur" and variable_name.strip() == "N"),
                                None) if variable_name.strip() == "N" else \
                            next((box['text'] for box in input_boxes if box['label'] == "Largeur" and variable_name.strip() == "M"),
                                None) if variable_name.strip() == "M" else \
                            next((box['text'] for box in input_boxes if box['label'] == variable_name.strip()), None)

                if new_value is not None:
                    line = f"{variable_name}= {new_value}\n"
            param_file.write(line)


# Entrées de texte
input_boxes = [
    {"rect": pygame.Rect(50, 50, 200, 32), "text": str(N), "label": "Longeur", "active": False},
    {"rect": pygame.Rect(50, 100, 200, 32), "text": str(M), "label": "Largeur", "active": False},
    {"rect": pygame.Rect(50, 150, 200, 32), "text": str(numberBob), "label": "numberBob", "active": False}
]

# Boutons
default_button = pygame.Rect(50, 250, 100, 50)
confirm_button = pygame.Rect(200, 250, 150, 50)

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gestion des événements de la souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in input_boxes:
                if box['rect'].collidepoint(event.pos):
                    box['active'] = not box['active']
                else:
                    box['active'] = False

            # Gestion des clics sur les boutons
            if default_button.collidepoint(event.pos):
                for box in input_boxes:
                    box['text'] = str(N) if box['label'] == "Longeur" else str(M) if box['label'] == "Largeur" else str(numberBob)
            elif confirm_button.collidepoint(event.pos):
                update_param_file()

        # Gestion des événements du clavier
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                for box in input_boxes:
                    if box['active'] and not is_number(box['text']):
                        box['text'] = str(N) if box['label'] == "Longeur" else str(M) if box['label'] == "Largeur" else str(numberBob)
                    box['active'] = False  # Désactive toutes les boîtes après l'entrée
            else:
                for box in input_boxes:
                    if box['active']:
                        if event.key == pygame.K_BACKSPACE:
                            box['text'] = box['text'][:-1]
                        else:
                            box['text'] += event.unicode

    # Effacer l'écran
    screen.fill(white)

    # Dessiner les boîtes de texte et les labels
    for box in input_boxes:
        if box['active'] and not is_number(box['text']):
            pygame.draw.rect(screen, light_red, box['rect'], 0)  # Fond rouge si la saisie n'est pas un nombre
        elif box['active']:
            pygame.draw.rect(screen, light_blue, box['rect'], 0)  # Fond bleu si la boîte est active
        else:
            pygame.draw.rect(screen, black, box['rect'], 2)
        text_surface = font.render(box['text'], True, black)
        width = max(200, text_surface.get_width() + 10)
        box['rect'].w = width
        screen.blit(text_surface, (box['rect'].x + 5, box['rect'].y + 5))

        # Dessiner le label à droite de la boîte
        label_surface = font.render(box['label'], True, black)
        screen.blit(label_surface, (box['rect'].x + box['rect'].w + 10, box['rect'].y + 5))

    # Dessiner les boutons
    pygame.draw.rect(screen, light_blue, default_button)
    pygame.draw.rect(screen, light_blue, confirm_button)

    # Dessiner le texte des boutons
    default_text = font.render("Default", True, black)
    screen.blit(default_text, (default_button.x + 10, default_button.y + 15))

    confirm_text = font.render("Confirmer", True, black)
    screen.blit(confirm_text, (confirm_button.x + 10, confirm_button.y + 15))

    # Mettre à jour l'affichage
    pygame.display.flip()
