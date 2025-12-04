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
        self.player = Player(self.keylistener, self.screen, 0, 0)
        self.map.add_player(self.player)

        # État du jeu : "world" (map principale) ou "loterie" (écran de loterie)
        self.game_state = "world"

    def run(self): # si le jeu est actif on fait quelque chose
        while self.running :
            self.handle_input()

            if self.game_state == "world":
                # Mettre à jour la map et le joueur
                self.map.update()
                
                if self.map.check_collision_with("maison_loterie", self.player):
                    self.game_state = "loterie"

            elif self.game_state == "loterie":
                # Gérer l'écran de loterie ici
                self.screen.get_display().fill((0, 0, 0))  # Fond noir

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
