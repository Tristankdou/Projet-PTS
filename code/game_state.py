import pygame
from code.map import Map
from code.player import Player
from battle import Battle
from code.lottery import Lottery
from code.cat import Cat
import random

class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.state = "EXPLORATION"  # EXPLORATION, BATTLE, LOTTERY
        
        # Zoom settings
        self.zoom = 2.0  # 2x zoom
        self.render_width = int(screen.get_width() / self.zoom)
        self.render_height = int(screen.get_height() / self.zoom)
        self.render_surface = pygame.Surface((self.render_width, self.render_height))
        
        # Initialize map
        self.map = Map("assets/map/map.tmx")
        
        # Initialize player with starting cat
        starting_cat = self.generate_random_cat()
        self.player = Player(200, 300, [starting_cat])
        self.player.coins = 10
        
        # Battle and lottery systems
        self.battle = None
        self.lottery = Lottery()
        
        # Camera offset
        self.camera_x = 0
        self.camera_y = 0
        
    def generate_random_cat(self):
        """Generate a random cat from the lottery pool"""
        cat_id = random.randint(1, 10)
        
        # Determine rarity
        rand = random.random()
        if rand < 0.10:  # 10% legendary
            rarity = "legendary"
        elif rand < 0.30:  # 20% rare (10% + 20%)
            rarity = "rare"
        else:  # 70% common
            rarity = "common"
        
        return Cat(
            cat_id=cat_id,
            rarity=rarity,
            x=0,
            y=0
        )
    
    def handle_event(self, event):
        if self.state == "EXPLORATION":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Check for trainer interaction
                    trainer = self.map.check_trainer_collision(self.player)
                    if trainer and not trainer.in_battle:
                        self.start_battle(trainer)
                    
                    # Check for lottery house
                    if self.map.check_lottery_collision(self.player):
                        self.state = "LOTTERY"
                        print("joueur dans loterie ")
        
        elif self.state == "BATTLE":
            self.battle.handle_event(event)
            if self.battle.battle_over:
                self.end_battle()
        
        elif self.state == "LOTTERY":
            result = self.lottery.handle_event(event, self.player)
            if result == "exit":
                self.state = "EXPLORATION"
            elif result is not None:
                # Player won a cat
                self.player.cats.append(result)
    
    def update(self, dt):
        if self.state == "EXPLORATION":
            keys = pygame.key.get_pressed()
            self.player.update(dt, keys, self.map)
            
            # Update camera to follow player
            self.update_camera()
            
            # Update trainers
            self.map.update_trainers(dt)
            
            # Random grass encounter for coins
            if self.map.is_on_grass(self.player):
                if random.random() < 0.001:  # Small chance per frame
                    coins_found = random.randint(1, 5)
                    self.player.coins += coins_found
                    print(f"Found {coins_found} coins in the grass!")
        
        elif self.state == "BATTLE":
            self.battle.update(dt)
    
    def update_camera(self):
        """Center camera on player"""
        screen_center_x = self.render_width // 2
        screen_center_y = self.render_height // 2
        
        self.camera_x = self.player.x - screen_center_x
        self.camera_y = self.player.y - screen_center_y
        
        # Clamp camera to map bounds
        max_x = self.map.width * self.map.tile_width - self.render_width
        max_y = self.map.height * self.map.tile_height - self.render_height
        
        self.camera_x = max(0, min(self.camera_x, max_x))
        self.camera_y = max(0, min(self.camera_y, max_y))
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if self.state == "EXPLORATION":
            # Draw to render surface (smaller resolution)
            self.render_surface.fill((0, 0, 0))
            
            # Draw map and entities with camera offset
            self.map.draw(self.render_surface, self.camera_x, self.camera_y)
            self.player.draw(self.render_surface, self.camera_x, self.camera_y)
            
            # Scale up the render surface to screen
            scaled_surface = pygame.transform.scale(
                self.render_surface,
                (self.screen.get_width(), self.screen.get_height())
            )
            self.screen.blit(scaled_surface, (0, 0))
            
            # Draw UI on top (not zoomed)
            self.draw_ui()
        
        elif self.state == "BATTLE":
            self.battle.draw(self.screen)
        
        elif self.state == "LOTTERY":
            self.lottery.draw(self.screen, self.player)
    
    def draw_ui(self):
        """Draw exploration UI (coins, team info)"""
        font = pygame.font.Font(None, 36)
        
        # Draw coins
        coin_text = font.render(f"Coins: {self.player.coins}", True, (255, 215, 0))
        self.screen.blit(coin_text, (10, 10))
        
        # Draw team size
        team_text = font.render(f"Team: {len(self.player.cats)}", True, (255, 255, 255))
        self.screen.blit(team_text, (10, 50))
        
        # Draw interaction hint
        small_font = pygame.font.Font(None, 24)
        hint_text = small_font.render("Press SPACE to interact", True, (200, 200, 200))
        self.screen.blit(hint_text, (10, self.screen.get_height() - 30))
    
    def start_battle(self, trainer):
        """Start a battle with a trainer"""
        # Let player choose a cat
        chosen_cat = self.choose_cat_for_battle()
        if chosen_cat:
            self.battle = Battle(chosen_cat, trainer.cat, self.player, trainer)
            self.state = "BATTLE"
            trainer.in_battle = True
    
    def choose_cat_for_battle(self):
        """Simple cat selection - return first cat for now"""
        if self.player.cats:
            return self.player.cats[0]
        return None
    
    def end_battle(self):
        """End battle and return to exploration"""
        if self.battle.winner == "player":
            # Player wins - gain coins and the trainer's cat
            self.player.coins += 20
            defeated_cat = self.battle.enemy_cat
            # Create a new cat instance (not the same reference)
            new_cat = Cat(
                cat_id=defeated_cat.cat_id,
                rarity=defeated_cat.rarity,
                x=0,
                y=0
            )
            self.player.cats.append(new_cat)
            print(f"Victory! Gained 20 coins and a new cat!")
        
        # Heal player's cat
        self.battle.player_cat.hp = self.battle.player_cat.max_hp
        
        self.state = "EXPLORATION"
        self.battle = None