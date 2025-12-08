import pygame

class Screen:
    def __init__(self):
        self.display = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Cat Wars")
        self.clock = pygame.time.Clock()
        self.framerate = 144
        self.deltatime = 0.0

    def update(self):
        pygame.display.flip()  # Met à jour l'affichage
        pygame.display.update()
        self.clock.tick(self.framerate)  # Contrôle les FPS
        self.deltatime = self.clock.get_time()

    def getdeltatime(self) :
        return self.deltatime

    def get_size(self) :
        return self.display.get_size()

    def get_display(self) :
        return self.display