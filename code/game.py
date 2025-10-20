import pygame

from screen import Screen
from map import Map

class Game:
    def __init__(self):
        self.running = True  # permet de voir si le jeu est actif
        self.screen = Screen()
        self.map = Map(self.screen)

    def run(self): # si le jeu est actif on fait quelque chose
        while self.running :
            self.map.update()
            self.screen.update() 