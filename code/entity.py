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
        self.rect : pygame.Rect = self.image.get_rect() #rectangle de collision de l'entité
        self.all_images = self.get_all_images() #toutes les images du personnage pour les animations
        self.index_image : int = 0  # index de l'image actuelle pour l'animation
        self.image_part = 0
        self.reset_animation = False

        self.hitbox: pygame.Rect = pygame.Rect(0, 0, 16, 16) #une hitbox est un rectangle invisible qui permet de détecter les collisions avec d'autres objets
        self.step : int = 0  # variable pour gérer les étapes d'animation
        self.animation_walk : bool = False  # variable pour savoir si l'entité est en train de marcher
        self.direction : str = "down"  # direction de l'entité (up, down, left, right)

        self.animation_step_time : int = 0.0  #pour stocker le temps
        self.action_animation = 16  #durée entre chaque étape d'animation en ms
        


    def update(self):
        self.animation_sprite()
        self.move()
        self.rect.topleft = self.position #mettre à jour la position du rectangle de collision
        self.hitbox.midbottom = self.rect.midbottom #midbottom car on veut que la hitbox se situe sur le corps de l'entité
        self.image = self.all_images[self.direction][self.index_image] #mettre à jour l'image de l'entité en fonction de la direction et de l'index de l'image

    def move_left(self) :
        self.animation_walk = True
        self.direction = "left"
    
    def move_right(self) :
        self.animation_walk = True
        self.direction = "right"

    def move_up(self) :
        self.animation_walk = True
        self.direction = "up"

    def move_down(self) :
        self.animation_walk = True
        self.direction = "down"

    def animation_sprite(self) :
        if int(self.step // 8) + self.image_part >= 4 :
            self.image_part = 0
            self.reset_animation = True
        self.index_image = int(self.step //8) + self.image_part # 4 images par direction, donc chaque image dure 8 étapes (16 pixels / 2)

    def move(self) :
        if self.animation_walk :
            self.animation_step_time += self.screen.getdeltatime()
            if self.step < 16 and self.animation_step_time >= self.action_animation : #car une case fait 16 pixels donc déplacement en 16
                self.step += 1
                if self.direction == "left" :
                    self.position.x -= 1
                elif self.direction == "right" :
                    self.position.x += 1
                elif self.direction == "up" :
                    self.position.y -= 1
                elif self.direction == "down" :
                    self.position.y += 1
                self.animation_step_time = 0.0 
            elif self.step >= 16 :
                self.step = 0
                self.animation_walk = False
                if self.reset_animation :
                    self.reset_animation = False
                else :
                    if self.image_part == 0 :
                        self.image_part = 2
                    else :
                        self.image_part = 0


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

        width : int = self.spritesheet.get_width() //4 #car 4 directions
        height : int = self.spritesheet.get_height() //4

        for j, key in enumerate(all_images.keys()):
            for i in range(4):  # 4 sprites par ligne
                x = i * width # Position x du sprite
                y = j * height # Position y du sprite
                sprite = Tool.split_image(self.spritesheet, x, y, 90, 150)
                sprite = pygame.transform.scale(sprite, (35, 55))
                all_images[key].append(sprite)
        return all_images