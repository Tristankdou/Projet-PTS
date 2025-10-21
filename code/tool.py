import pygame

class Tool:
    @staticmethod
    def split_image(spritesheet, x, y, width, height):
        if x + width > spritesheet.get_width() or y + height > spritesheet.get_height():
            raise ValueError(f"Les coordonnées ou dimensions dépassent la taille de la spritesheet.")
        return spritesheet.subsurface(pygame.Rect(x, y, width, height))