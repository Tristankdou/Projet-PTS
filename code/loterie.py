import pygame

class LoterieScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)  # Taille du titre
        self.button_font = pygame.font.SysFont("Arial", 28)  # Taille du bouton

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

        # Bouton "Jouer" centré en bas
        self.jouer_button = pygame.Rect(450, 550, 300, 70)  # Centré horizontalement

    def afficher(self):
        """Affiche l'écran de loterie avec l'image de fond et le bouton 'Jouer'."""
        # Afficher l'image de fond
        self.screen.get_display().blit(self.background, (0, 0))

        # Titre en haut à gauche
        title = self.font.render("Loterie des Chats", True, self.text_color)
        self.screen.get_display().blit(title, (50, 30))  # Position en haut à gauche

        # Dessiner le bouton "Jouer" (centré en bas)
        mouse_pos = pygame.mouse.get_pos()
        jouer_color = self.button_hover_color if self.jouer_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen.get_display(), jouer_color, self.jouer_button, border_radius=10)
        jouer_text = self.button_font.render("Jouer", True, self.text_color)

        # Centrer le texte dans le bouton
        text_rect = jouer_text.get_rect(center=self.jouer_button.center)
        self.screen.get_display().blit(jouer_text, text_rect)

        # Instructions pour quitter
        instruction = self.button_font.render("Appuyez sur Q pour quitter", True, self.text_color)
        self.screen.get_display().blit(instruction, (450, 650))

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return "world"  # Quitter avec Q

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.jouer_button.collidepoint(mouse_pos):
                    print("Bouton Jouer cliqué !")  # TODO : Lancer le tirage

        return "loterie"  # Rester dans la loterie
