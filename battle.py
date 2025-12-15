import pygame

class Battle:
    def __init__(self, player_cat, enemy_cat, player, trainer):
        self.player_cat = player_cat
        self.enemy_cat = enemy_cat
        self.player = player
        self.trainer = trainer
        
        # Battle state
        self.turn = "player"  # player or enemy
        self.battle_over = False
        self.winner = None
        
        # UI state
        self.selected_move = 0
        self.moves = ["Attaque Normale", "Attaque Speciale"]
        self.message = "Quelle attaque choisissez-vous ?"
        self.message_timer = 0
        self.waiting_for_input = True
        
        # Animation
        self.shake_timer = 0
        self.shake_target = None
    
    def handle_event(self, event):
        
        if not self.waiting_for_input or self.battle_over:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_move = max(0, self.selected_move - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_move = min(len(self.moves) - 1, self.selected_move + 1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.execute_player_turn()
    
    def execute_player_turn(self):
        """execute l'attaque du joueur"""
        self.waiting_for_input = False
        
        use_special = (self.selected_move == 1)
        damage = self.player_cat.calculate_damage(self.enemy_cat, use_special)
        self.enemy_cat.take_damage(damage)
        
        move_name = "Attaque Speciale " if use_special else "Attaque Normale"
        self.message = f"Votre chat a utilisé {move_name} ! et a infligé {damage} dégâts!"
        self.shake_target = "enemy"
        self.shake_timer = 0.3
        
        # Check if enemy defeated
        if not self.enemy_cat.is_alive():
            self.message = "Vous avez gagné !!"
            self.battle_over = True
            self.winner = "player"
            self.trainer.defeat()
        else:
            self.turn = "enemy"
    
    def execute_enemy_turn(self):
        """Execute enemy's turn"""
        import random
        use_special = random.choice([False, True])
        damage = self.enemy_cat.calculate_damage(self.player_cat, use_special)
        self.player_cat.take_damage(damage)
        
        move_name = "Attaque Speciale" if use_special else "Attaque Normale"
        self.message = f"Le chat énemi a utilisé {move_name}! Il a infligé {damage} dégâts!"
        self.shake_target = "player"
        self.shake_timer = 0.3
        
        # Check if player defeated
        if not self.player_cat.is_alive():
            self.message = "Vous avez perdu..."
            self.battle_over = True
            self.winner = "enemy"
        else:
            self.turn = "player"
            self.waiting_for_input = True
    
    def update(self, dt):
        """Update battle state"""
        # Handle shake animation
        if self.shake_timer > 0:
            self.shake_timer -= dt
        
        # Auto-advance enemy turn
        if self.turn == "enemy" and not self.battle_over:
            if self.message_timer > 1.5:
                self.execute_enemy_turn()
                self.message_timer = 0
            else:
                self.message_timer += dt
        
        # Reset message timer for player turn
        if self.turn == "player" and not self.waiting_for_input:
            if self.message_timer > 1.5:
                self.message_timer = 0
                self.waiting_for_input = True
                self.message = "What will you do?"
            else:
                self.message_timer += dt
    
    def draw(self, screen):
        """Draw battle screen"""
        screen.fill((50, 50, 100))
        
        # Calculate positions
        player_x = 150
        player_y = 400
        enemy_x = 850
        enemy_y = 200
        
        # Apply shake effect
        shake_offset = 0
        if self.shake_timer > 0:
            import random
            shake_offset = random.randint(-5, 5)
        
        # Draw cats
        if self.shake_target == "player":
            self.player_cat.draw_battle_sprite(screen, player_x + shake_offset, player_y)
        else:
            self.player_cat.draw_battle_sprite(screen, player_x, player_y)
        
        if self.shake_target == "enemy":
            self.enemy_cat.draw_battle_sprite(screen, enemy_x + shake_offset, enemy_y)
        else:
            self.enemy_cat.draw_battle_sprite(screen, enemy_x, enemy_y)
        
        # Draw HP bars
        self.draw_hp_bar(screen, player_x, player_y - 30, self.player_cat, "Your Cat")
        self.draw_hp_bar(screen, enemy_x, enemy_y - 30, self.enemy_cat, "Enemy Cat")
        
        # Draw battle UI
        self.draw_battle_ui(screen)
    
    def draw_hp_bar(self, screen, x, y, cat, label):
        """Draw HP bar for a cat"""
        font = pygame.font.Font(None, 24)
        
        # Label
        label_surf = font.render(label, True, (255, 255, 255))
        screen.blit(label_surf, (x, y - 25))
        
        # HP bar background
        bar_width = 150
        bar_height = 15
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_width, bar_height))
        
        # HP bar fill
        hp_ratio = cat.hp / cat.max_hp
        fill_width = int(bar_width * hp_ratio)
        
        if hp_ratio > 0.5:
            color = (0, 255, 0)
        elif hp_ratio > 0.2:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        
        pygame.draw.rect(screen, color, (x, y, fill_width, bar_height))
        
        # HP text
        hp_text = font.render(f"{cat.hp}/{cat.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (x + bar_width + 10, y - 3))
    
    def draw_battle_ui(self, screen):
        """Draw battle menu and messages"""
        # Message box
        msg_box = pygame.Rect(50, 550, 1100, 100)
        pygame.draw.rect(screen, (30, 30, 60), msg_box)
        pygame.draw.rect(screen, (255, 255, 255), msg_box, 3)
        
        font = pygame.font.Font(None, 32)
        msg_surf = font.render(self.message, True, (255, 255, 255))
        screen.blit(msg_surf, (70, 580))
        
        # Move selection menu (only during player turn)
        if self.turn == "player" and self.waiting_for_input and not self.battle_over:
            menu_box = pygame.Rect(700, 350, 450, 180)
            pygame.draw.rect(screen, (30, 30, 60), menu_box)
            pygame.draw.rect(screen, (255, 255, 255), menu_box, 3)
            
            for i, move in enumerate(self.moves):
                color = (255, 255, 0) if i == self.selected_move else (255, 255, 255)
                move_surf = font.render(f"> {move}" if i == self.selected_move else move, True, color)
                screen.blit(move_surf, (730, 370 + i * 50))
        
        # Battle over message
        if self.battle_over:
            overlay = pygame.Surface((1200, 700), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            result_font = pygame.font.Font(None, 72)
            result_text = "VICTORY!" if self.winner == "player" else "DEFEAT!"
            result_color = (0, 255, 0) if self.winner == "player" else (255, 0, 0)
            result_surf = result_font.render(result_text, True, result_color)
            
            rect = result_surf.get_rect(center=(600, 250))
            screen.blit(result_surf, rect)
            
            # Instructions
            inst_font = pygame.font.Font(None, 32)
            inst_surf = inst_font.render("Press any key to continue", True, (255, 255, 255))
            inst_rect = inst_surf.get_rect(center=(600, 350))
            screen.blit(inst_surf, inst_rect)
