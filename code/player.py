import pygame
from code.entity import Entity

class Player(Entity):
    def __init__(self, x, y, starting_cats):
        super().__init__(x, y, "assets/sprites/boy_character.png")
        
        self.speed = 60  # pixels per second
        self.direction = "down"  # up, down, left, right
        self.moving = False
        
        # Player stats
        self.cats = starting_cats
        self.coins = 0
        
        # Hitbox - smaller than sprite for better collision feel
        self.hitbox_width = 16
        self.hitbox_height = 16
        self.hitbox_offset_x = (self.width - self.hitbox_width) // 2
        self.hitbox_offset_y = self.height - self.hitbox_height  # Bottom-aligned
        
        # Animation rows for each direction
        self.direction_rows = {
            "down": 0,
            "left": 1,
            "right": 2,
            "up": 3
        }
    
    def update(self, dt, keys, game_map):
        """Update player position and animation"""
        dx = 0
        dy = 0
        self.moving = False
        
        # Handle input
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed * dt
            self.direction = "up"
            self.moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed * dt
            self.direction = "down"
            self.moving = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed * dt
            self.direction = "left"
            self.moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed * dt
            self.direction = "right"
            self.moving = True
        
        # Try to move and check collisions using hitbox
        if dx != 0:
            new_x = self.x + dx
            hitbox_x = new_x + self.hitbox_offset_x
            hitbox_y = self.y + self.hitbox_offset_y
            if not game_map.is_collision(hitbox_x, hitbox_y, self.hitbox_width, self.hitbox_height):
                self.x = new_x
        
        if dy != 0:
            new_y = self.y + dy
            hitbox_x = self.x + self.hitbox_offset_x
            hitbox_y = new_y + self.hitbox_offset_y
            if not game_map.is_collision(hitbox_x, hitbox_y, self.hitbox_width, self.hitbox_height):
                self.y = new_y
        
        # Update animation
        if self.moving:
            self.update_animation(dt)
        else:
            self.current_frame = 0  # Idle frame
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw player with current direction"""
        if self.sprite_sheet:
            row = self.direction_rows[self.direction]
            frame = self.get_current_frame(row)
            if frame:
                # Scale frame to player size
                scaled_frame = pygame.transform.scale(frame, (self.width, self.height))
                screen.blit(scaled_frame, (self.x - camera_x, self.y - camera_y))
        else:
            # Fallback
            pygame.draw.rect(
                screen,
                (0, 0, 255),
                (self.x - camera_x, self.y - camera_y, self.width, self.height)
            )