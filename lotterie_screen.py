import pygame
from cat import Cat
import random

class LoterieScreen:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.SysFont("Arial", 36)
        self.button_font = pygame.font.SysFont("Arial", 28)

        # Couleurs
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 170, 220)
        self.text_color = (255, 255, 255)

        # Charger l'image de fond
        # ATTENTION: Vérifie si ton dossier s'appelle "sprite" ou "sprites" (avec s)
        try:
            self.background = pygame.image.load("assets/sprites/loterie.png").convert()
            self.background = pygame.transform.scale(self.background, (1200, 700))
        except FileNotFoundError:
            print("Erreur : Image de fond introuvable. Fond bleu utilisé.")
            self.background = pygame.Surface((1200, 700))
            self.background.fill((20, 20, 50))

        # Bouton "Jouer" centré en bas
        self.jouer_button = pygame.Rect(450, 550, 300, 70)
        self.obtenu_cat = None
        self.cost = 10 

    def handle_input(self, event):
        """Gère les entrées (clics, touches) et retourne une action"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.jouer_button.collidepoint(mouse_pos):
                if self.player.coins >= self.cost:
                    self.player.coins -= self.cost
                    self.obtenu_cat = self.generate_random_cat()
                    return self.obtenu_cat  # Retourne le chat gagné
                else:
                    print("Pas assez de pièces !")
        
        return None

    def draw(self):
        """Affiche l'écran de loterie"""
        self.screen.blit(self.background, (0, 0))

        # Titre
        title = self.font.render("Loterie des Chats", True, self.text_color)
        self.screen.blit(title, (50, 30))

        # Pièces
        pieces_text = self.font.render(f"Pièces: {self.player.coins}", True, self.text_color)
        self.screen.blit(pieces_text, (50, 80))

        # Chat obtenu
        if self.obtenu_cat:
            # On utilise les coordonnées fixes pour l'affichage
            self.obtenu_cat.draw_loterie_sprite(self.screen, 536, 250, size=128)
            
            # Info du chat
            cat_name = f"{self.obtenu_cat.rarity.capitalize()} Cat #{self.obtenu_cat.cat_id}"
            cat_info = self.font.render(cat_name, True, self.text_color)
            
            # Centrer le texte sous le chat
            text_rect = cat_info.get_rect(center=(600, 400))
            self.screen.blit(cat_info, text_rect)

        # Bouton Jouer
        mouse_pos = pygame.mouse.get_pos()
        jouer_color = self.button_hover_color if self.jouer_button.collidepoint(mouse_pos) else self.button_color
        pygame.draw.rect(self.screen, jouer_color, self.jouer_button, border_radius=10)
        
        jouer_text = self.button_font.render(f"Jouer ({self.cost} pièces)", True, self.text_color)
        text_rect = jouer_text.get_rect(center=self.jouer_button.center)
        self.screen.blit(jouer_text, text_rect)

        # Instructions
        instruction = self.button_font.render("Appuyez sur Q pour quitter", True, self.text_color)
        inst_rect = instruction.get_rect(center=(600, 660))
        self.screen.blit(instruction, inst_rect)

    def generate_random_cat(self):
        cat_id = random.randint(1, 10)
        rand = random.random()
        if rand < 0.10: rarity = "legendary"
        elif rand < 0.30: rarity = "rare"
        else: rarity = "common"
        return Cat(cat_id=cat_id, rarity=rarity, x=0, y=0)