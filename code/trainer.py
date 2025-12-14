import pygame
from code.entity import Entity
from code.cat import Cat
import random

class Trainer(Entity):
    def __init__(self, x, y):
        # Trainers are just cats on the map
        cat_id = random.randint(1, 10)
        
        # Random rarity for trainer cats
        rand = random.random()
        if rand < 0.10:
            rarity = "legendary"
        elif rand < 0.30:
            rarity = "rare"
        else:
            rarity = "common"
        
        sprite_path = f"assets/sprites/cat_sprite_{cat_id}.jpg"
        super().__init__(x, y, sprite_path)
        
        self.cat = Cat(cat_id, rarity, x, y)
        self.visible = True
        self.in_battle = False
        
        # Respawn timer
        self.respawn_timer = 0
        self.respawn_delay = 60.0  # 60 seconds
    
    def update(self, dt):
        """Update trainer state and respawn timer"""
        if not self.visible:
            self.respawn_timer += dt
            if self.respawn_timer >= self.respawn_delay:
                self.respawn()
        else:
            # Animate when visible
            self.update_animation(dt)
    
    def respawn(self):
        """Respawn the trainer"""
        self.visible = True
        self.in_battle = False
        self.respawn_timer = 0
        
        # Generate new cat
        cat_id = random.randint(1, 10)
        rand = random.random()
        if rand < 0.10:
            rarity = "legendary"
        elif rand < 0.30:
            rarity = "rare"
        else:
            rarity = "common"
        
        self.cat = Cat(cat_id, rarity, self.x, self.y)
    
    def defeat(self):
        """Mark trainer as defeated"""
        self.visible = False
        self.in_battle = False
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw trainer cat on map"""
        if self.visible and self.sprite_sheet:
            frame = self.get_current_frame(0)
            if frame:
                scaled = pygame.transform.scale(frame, (self.width, self.height))
                screen.blit(scaled, (self.x - camera_x, self.y - camera_y))
                
                # Draw rarity indicator above trainer
                color = self.cat.get_rarity_color()
                pygame.draw.circle(
                    screen,
                    color,
                    (int(self.x - camera_x + self.width // 2), int(self.y - camera_y - 5)),
                    4
                )
