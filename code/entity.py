import pygame

from tool import Tool
from keylistener import KeyListener

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener : KeyListener):
        super().__init__() #initialiser la classe parente pygame.sprite.Sprite
        self.keylistener = keylistener
        self.spritesheet = pygame.image.load("../assets/sprite/Boy_character.png") #charger la spritesheet
        self.image = Tool.split_image(self.spritesheet, 0, 0, 90, 150) #découper la spritesheet pour obtenir le personnage

        # Redimensionner le sprite
        new_width, new_height = 35, 55
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.position = [0, 0] #position de l'entité
        #self.rect : pygame.Rect = pygame.Rect(0, 0, 16, 32) #rectangle de collision de l'entité
        self.rect = self.image.get_rect(topleft=self.position)
        self.all_images = self.get_all_images() #toutes les images du personnage pour les animations

    def update(self):
        self.check_move()
        self.rect.topleft = self.position #mettre à jour la position du rectangle de collision

    def check_move(self):
        if self.keylistener.key_pressed(pygame.K_LEFT) :
            self.move_left()
        if self.keylistener.key_pressed(pygame.K_RIGHT) :
            self.move_right()
        if self.keylistener.key_pressed(pygame.K_UP) :
            self.move_up()
        if self.keylistener.key_pressed(pygame.K_DOWN) :
            self.move_down()

    def move_left(self) :
        self.position[0] -= 1
        self.image = self.all_images["left"][0]
    
    def move_right(self) :
        self.position[0] += 1
        self.image = self.all_images["right"][0]

    def move_up(self) :
        self.position[1] -= 1
        self.image = self.all_images["up"][0]

    def move_down(self) :
        self.position[1] += 1
        self.image = self.all_images["down"][0]

    def get_all_images(self):
        all_images = {"down": [], "left": [], "right": [], "up": []}
        for j, key in enumerate(all_images.keys()):
            for i in range(4):  # 4 sprites par ligne
                x = i  # Position x du sprite
                y = j * 155  # Position y du sprite
                sprite = Tool.split_image(self.spritesheet, x, y, 90, 150)
                sprite = pygame.transform.scale(sprite, (35, 55))
                all_images[key].append(sprite)
        return all_images


