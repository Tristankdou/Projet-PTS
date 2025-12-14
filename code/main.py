import pygame
import sys
from code.game_state import GameState
import code.player as player

def main():
    pygame.init()
    
    # Window settings
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cat Wars")
    
    clock = pygame.time.Clock()
    FPS = 60
    
    # Initialize game state
    game_state = GameState(screen)
    
    # Main game loop
    running = True
    while running:
        # if game_state.map.is_collision(game_state.player.x, game_state.player.y, game_state.player.width, game_state.player.height):
        #     print("Collision detected at player position!")
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            game_state.handle_event(event)
        
        game_state.update(dt)
        game_state.draw()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
