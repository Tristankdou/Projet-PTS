import pygame
import random
from code.cat import Cat

class Lottery:
    def __init__(self):
        self.cost = 15
        self.result_cat = None
        self.show_result = False
        self.result_timer = 0
        
        # Animation
        self.spin_timer = 0
        self.spinning = False
        self.spin_duration = 2.0
    
    def handle_event(self, event, player):
        """Handle lottery input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "exit"
            
            if not self.spinning and not self.show_result:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if player.coins >= self.cost:
                        self.start_lottery(player)
                    else:
                        print("Not enough coins!")
            
            elif self.show_result:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Claim the cat
                    cat_to_return = self.result_cat
                    self.result_cat = None
                    self.show_result = False
                    return cat_to_return
        
        return None
    
    def start_lottery(self, player):
        """Start the lottery spin"""
        player.coins -= self.cost
        self.spinning = True
        self.spin_timer = 0
        self.show_result = False
    
    def update(self, dt):
        """Update lottery animation"""
        if self.spinning:
            self.spin_timer += dt
            if self.spin_timer >= self.spin_duration:
                self.spinning = False
                self.show_result = True
                self.result_cat = self.generate_lottery_cat()
    
    def generate_lottery_cat(self):
        """Generate a random cat from lottery"""
        cat_id = random.randint(1, 10)
        
        # Rarity distribution
        rand = random.random()
        if rand < 0.10:  # 10% legendary
            rarity = "legendary"
        elif rand < 0.30:  # 20% rare
            rarity = "rare"
        else:  # 70% common
            rarity = "common"
        
        return Cat(cat_id, rarity, 0, 0)
    
    def draw(self, screen, player):
        """Draw lottery screen"""
        screen.fill((20, 20, 40))
        
        # Title
        title_font = pygame.font.Font(None, 72)
        title_surf = title_font.render("CAT LOTTERY", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(600, 80))
        screen.blit(title_surf, title_rect)
        
        # Player coins
        coin_font = pygame.font.Font(None, 48)
        coin_surf = coin_font.render(f"Your Coins: {player.coins}", True, (255, 255, 255))
        coin_rect = coin_surf.get_rect(center=(600, 160))
        screen.blit(coin_surf, coin_rect)
        
        # Cost
        cost_font = pygame.font.Font(None, 36)
        cost_surf = cost_font.render(f"Cost: {self.cost} coins", True, (200, 200, 200))
        cost_rect = cost_surf.get_rect(center=(600, 220))
        screen.blit(cost_surf, cost_rect)
        
        if self.spinning:
            # Spinning animation
            self.draw_spinning_animation(screen)
        
        elif self.show_result:
            # Show result
            self.draw_result(screen)
        
        else:
            # Instructions
            inst_font = pygame.font.Font(None, 32)
            
            if player.coins >= self.cost:
                inst_surf = inst_font.render("Press ENTER to spin!", True, (0, 255, 0))
            else:
                inst_surf = inst_font.render("Not enough coins!", True, (255, 0, 0))
            
            inst_rect = inst_surf.get_rect(center=(600, 400))
            screen.blit(inst_surf, inst_rect)
            
            esc_surf = inst_font.render("Press ESC to exit", True, (200, 200, 200))
            esc_rect = esc_surf.get_rect(center=(600, 450))
            screen.blit(esc_surf, esc_rect)
    
    def draw_spinning_animation(self, screen):
        """Draw lottery spinning animation"""
        font = pygame.font.Font(None, 64)
        
        # Spinning text
        dots = "." * (int(self.spin_timer * 5) % 4)
        spin_surf = font.render(f"SPINNING{dots}", True, (255, 255, 0))
        spin_rect = spin_surf.get_rect(center=(600, 350))
        screen.blit(spin_surf, spin_rect)
        
        # Random cat previews flashing
        preview_y = 450
        for i in range(5):
            cat_id = random.randint(1, 10)
            x = 200 + i * 180
            
            # Simple colored box as preview
            color = random.choice([(150, 150, 150), (100, 150, 255), (255, 215, 0)])
            pygame.draw.rect(screen, color, (x, preview_y, 80, 80))
            
            small_font = pygame.font.Font(None, 24)
            id_surf = small_font.render(f"Cat {cat_id}", True, (255, 255, 255))
            screen.blit(id_surf, (x + 5, preview_y + 30))
    
    def draw_result(self, screen):
        """Draw lottery result"""
        result_font = pygame.font.Font(None, 64)
        result_surf = result_font.render("YOU WON!", True, (0, 255, 0))
        result_rect = result_surf.get_rect(center=(600, 280))
        screen.blit(result_surf, result_rect)
        
        # Draw the won cat
        if self.result_cat:
            cat_x = 550
            cat_y = 350
            self.result_cat.draw_battle_sprite(screen, cat_x, cat_y, 128)
            
            # Cat info
            info_font = pygame.font.Font(None, 36)
            
            rarity_text = f"Rarity: {self.result_cat.rarity.upper()}"
            rarity_color = self.result_cat.get_rarity_color()
            rarity_surf = info_font.render(rarity_text, True, rarity_color)
            screen.blit(rarity_surf, (480, 500))
            
            stats_text = f"HP: {self.result_cat.hp} | ATK: {self.result_cat.attack} | DEF: {self.result_cat.defense}"
            stats_surf = info_font.render(stats_text, True, (255, 255, 255))
            screen.blit(stats_surf, (350, 540))
        
        # Instructions
        inst_font = pygame.font.Font(None, 32)
        inst_surf = inst_font.render("Press ENTER to claim your cat!", True, (200, 200, 200))
        inst_rect = inst_surf.get_rect(center=(600, 600))
        screen.blit(inst_surf, inst_rect)
