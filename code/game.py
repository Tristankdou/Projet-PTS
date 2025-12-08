import pygame

from screen import Screen
from map import Map
from entity import Entity
from keylistener import KeyListener
from player import Player

class Game:
    def __init__(self):
        self.running = True  # permet de voir si le jeu est actif
        self.screen = Screen()
        self.map = Map(self.screen)
        self.keylistener = KeyListener()
        self.player = Player(self.keylistener, self.screen, 380, 300)
        self.map.add_player(self.player)

        # État du jeu : "world" (map principale) ou "loterie" (écran de loterie)
        self.game_state = "world"

        try:
            self.loterie_background = pygame.image.load("../assets/sprite/loterie.png").convert()
            self.loterie_background = pygame.transform.scale(self.loterie_background, (1200, 700))
        except FileNotFoundError:
            print("Erreur : Image de fond introuvable. Utilisation d'un fond noir.")
            self.loterie_background = None  # Utilisera un fond noir en cas d'erreur

    def run(self):
        while self.running:
            self.handle_input()

            if self.game_state == "world":
                self.map.update()
                self.map.group.draw(self.screen.get_display())

            # Détecter la collision avec la maison
                if self.map.check_collision_with("maison_loterie", self.player):
                    self.game_state = "loterie"

            elif self.game_state == "loterie":
                # Afficher l'image de fond ou un fond noir
                if self.loterie_background:
                    self.screen.get_display().blit(self.loterie_background, (0, 0))
                else:
                    self.screen.get_display().fill((0, 0, 0))  # Fond noir en secours

            self.screen.update()

    def handle_input(self) :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT : #si on clique sur la croix on ferme le jeu
                pygame.quit()
            elif event.type == pygame.KEYDOWN :
                self.keylistener.add_key(event.key)
            elif event.type == pygame.KEYUP :
                self.keylistener.remove_key(event.key)

    def update(self):
        if self.game_state == "world":
        # Mettre à jour la map et le joueur
            self.map.update()

        # Détecter la collision avec la maison (à adapter selon ta classe Map)
        if self.map.check_collision_with("maison_loterie", self.player):
            self.game_state = "loterie"