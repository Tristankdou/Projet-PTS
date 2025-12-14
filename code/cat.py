import pygame
from code.entity import Entity

class Cat(Entity):
    def __init__(self, cat_id, rarity, x, y):
        sprite_path = f"assets/sprites/cat_sprite_{cat_id}.jpg"
        super().__init__(x, y, sprite_path)
        
        self.cat_id = cat_id
        self.rarity = rarity
        
        # Stats based on rarity
        self.setup_stats()
        
        self.max_hp = self.hp
    
    def setup_stats(self):
        """Set stats based on rarity"""
        if self.rarity == "common":
            self.hp = 50 + (self.cat_id * 5)
            self.attack = 10 + (self.cat_id * 2)
            self.defense = 5 + self.cat_id
            self.special_attack = 8 + (self.cat_id * 2)
        elif self.rarity == "rare":
            self.hp = 80 + (self.cat_id * 8)
            self.attack = 15 + (self.cat_id * 3)
            self.defense = 10 + (self.cat_id * 2)
            self.special_attack = 12 + (self.cat_id * 3)
        else:  # legendary
            self.hp = 120 + (self.cat_id * 10)
            self.attack = 25 + (self.cat_id * 4)
            self.defense = 15 + (self.cat_id * 3)
            self.special_attack = 20 + (self.cat_id * 4)
    
    def calculate_damage(self, target, use_special=False):
        """Calculate damage dealt to target"""
        if use_special:
            raw_damage = self.special_attack * 2
        else:
            raw_damage = self.attack
        
        # Apply defense
        damage = max(1, raw_damage - target.defense)
        return damage
    
    def take_damage(self, damage):
        """Reduce HP by damage amount"""
        self.hp = max(0, self.hp - damage)
    
    def is_alive(self):
        """Check if cat is still alive"""
        return self.hp > 0
    
    def get_rarity_color(self):
        """Get color based on rarity"""
        if self.rarity == "common":
            return (150, 150, 150)  # Gray
        elif self.rarity == "rare":
            return (100, 150, 255)  # Blue
        else:  # legendary
            return (255, 215, 0)  # Gold
    
    def draw_battle_sprite(self, screen, x, y, size=128):
        """Draw cat sprite for battle screen"""
        self.update_animation(0.016)  # Animate
        
        if self.sprite_sheet:
            frame = self.get_current_frame(0)
            if frame:
                scaled = pygame.transform.scale(frame, (size, size))
                screen.blit(scaled, (x, y))
        else:
            # Fallback
            pygame.draw.rect(screen, (255, 0, 255), (x, y, size, size))
        
        # Draw rarity indicator
        color = self.get_rarity_color()
        pygame.draw.circle(screen, color, (x + size - 10, y + 10), 8)
