import pygame

from tool import Tool
from screen import Screen
from keylistener import KeyListener

class Entity(pygame.sprite.Sprite):
    def __init__(self, keylistener : KeyListener, screen: Screen,x: int, y: int):
        super().__init__() #initialiser la classe parente pygame.sprite.Sprite
        self.screen = screen
        self.keylistener = keylistener
        self.spritesheet = pygame.image.load("../assets/sprite/Boy_character.png") #charger la spritesheet
        self.image = Tool.split_image(self.spritesheet, 0, 0, 90, 150) #découper la spritesheet pour obtenir le personnage

        # Redimensionner le sprite
        new_width, new_height = 35, 55
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.position : pygame.math.Vector2 = pygame.math.Vector2(x,y) #position de l'entité
        #self.rect : pygame.Rect = pygame.Rect(0, 0, 16, 32) #rectangle de collision de l'entité
        self.rect = self.image.get_rect(topleft=self.position)
        self.all_images = self.get_all_images() #toutes les images du personnage pour les animations

        self.hitbox: pygame.Rect = pygame.Rect(0, 0, 16, 16) #une hitbox est un rectangle invisible qui permet de détecter les collisions avec d'autres objets


    def update(self):
        self.rect.topleft = self.position #mettre à jour la position du rectangle de collision
        self.hitbox.midbottom = self.rect.midbottom #midbottom car on veut que la hitbox se situe sur le corps de l'entité

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

    def align_hitbox(self) :
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.x % 16 != 0 :
            self.rect.x -= 1
            self.hitbox.midbottom = self.rect.midbottom
        while self.hitbox.y % 16 != 0 :
            self.rect.y -= 1
            self.hitbox.midbottom = self.rect.midbottom
        self.position = pygame.math.Vector2(self.rect.center)

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