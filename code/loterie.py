import pygame

class LoterieScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)
        self.button_font = pygame.font.SysFont("Arial", 24)

        # Couleurs des boutons
        self.button_color = (70, 130, 180)  # Bleu clair
        self.button_hover_color = (100, 170, 220)  # Bleu plus clair au survol
        self.text_color = (255, 255, 255)  # Blanc

        # Charger l'image de fond
        try:
            self.background = pygame.image.load("../assets/sprite/loterie.png").convert()
            self.background = pygame.transform.scale(self.background, (1200, 700))
        except FileNotFoundError:
            print("Erreur : Image de fond introuvable. Utilisation d'un fond bleu.")
            self.background = pygame.Surface((1200, 700))
            self.background.fill((20, 20, 50))  # Fond bleu en secours

        # Boutons
        self.jouer_button = pygame.Rect(450, 500, 300, 70)
        self.quitter_button = pygame.Rect(450, 600, 300, 70)

    def afficher(self):
        """Affiche l'écran de loterie avec l'image de fond et les boutons."""
        # Afficher l'image de fond
        self.screen.get_display().blit(self.background, (0, 0))

        # Titre (optionnel)
        title = self.font.render("Loterie des Chats", True, self.text_color)
        self.screen.get_display().blit(title, (450, 50))

        # Dessiner les boutons
        mouse_pos = pygame.mouse.get_pos()

        # Bouton "Jouer"
        jouer_color = self.button_hover_color if self.jouer_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen.get_display(), jouer_color, self.jouer_button, border_radius=10)
        jouer_text = self.button_font.render("Jouer", True, self.text_color)
        self.screen.get_display().blit(jouer_text, (550, 520))

        # Bouton "Quitter"
        quitter_color = self.button_hover_color if self.quitter_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen.get_display(), quitter_color, self.quitter_button, border_radius=10)
        quitter_text = self.button_font.render("Quitter", True, self.text_color)
        self.screen.get_display().blit(quitter_text, (540, 620))

        # Instructions
        instruction = self.button_font.render("Appuyez sur Q pour quitter", True, self.text_color)
        self.screen.get_display().blit(instruction, (450, 680))

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return "world"  # Quitter avec Q

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.jouer_button.collidepoint(mouse_pos):
                    print("Bouton Jouer cliqué !")  # TODO : Lancer le tirage
                elif self.quitter_button.collidepoint(mouse_pos):
                    return "world"  # Retour à la map

        return "loterie"  # Rester dans la loterie
