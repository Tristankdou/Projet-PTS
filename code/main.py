import pygame

from game import Game

# Initialisation de Pygame
pygame.init()

if __name__ == "__main__":  # si le nom du fichier est main on lance le programme
    game = Game()
    game.run()
