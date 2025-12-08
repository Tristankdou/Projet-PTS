import pygame

class LoterieScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)

        # Charger l'image de fond
        try:
            self.background = pygame.image.load("assets/loterie.png").convert()
            self.background = pygame.transform.scale(self.background, (1200, 700))  # Redimensionner
        except FileNotFoundError:
            print("Erreur : Image de fond introuvable. Utilisation d'un fond noir.")
            self.background = pygame.Surface((1200, 700))
            self.background.fill((50, 50, 50))  # Fond gris si l'image est manquante

    def afficher(self):
        """Affiche la fenêtre de loterie avec une image de fond et un bouton 'Jouer'."""
        # Afficher l'image de fond
        self.screen.get_display().blit(self.background, (0, 0))

        # Bouton "Jouer" (centré en bas)
        jouer_button = pygame.Rect(500, 550, 200, 60)
        pygame.draw.rect(self.screen.get_display(), (0, 200, 0), jouer_button)
        text = self.font.render("Jouer", True, (0, 0, 0))
        self.screen.get_display().blit(text, (570, 570))

        # Texte d'instruction pour quitter
        quit_text = self.font.render("Appuyez sur Q pour quitter", True, (255, 255, 255))
        self.screen.get_display().blit(quit_text, (450, 650))

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return "world"  # Quitter avec Q

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_pos = pygame.mouse.get_pos()
                    if jouer_button.collidepoint(mouse_pos):
                        print("Bouton Jouer cliqué !")
                        return "loterie"  # Rester dans la loterie

        return "loterie"  # Rester dans la loterie