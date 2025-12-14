import pygame

class Entity:
    def __init__(self, x, y, sprite_path=None):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        
        # Sprite and animation
        self.sprite_sheet = None
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15  # seconds per frame
        
        if sprite_path:
            self.load_sprite(sprite_path)
    
    def load_sprite(self, path):
        """Load sprite sheet"""
        try:
            self.sprite_sheet = pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Could not load sprite: {path}")
            # Create placeholder
            self.sprite_sheet = pygame.Surface((64, 64))
            self.sprite_sheet.fill((255, 0, 255))
    
    def get_current_frame(self, row, num_frames=4):
        """Extract current animation frame from sprite sheet"""
        if self.sprite_sheet is None:
            return None
        
        frame_width = self.sprite_sheet.get_width() // num_frames
        frame_height = self.sprite_sheet.get_height() // 4  # Assuming 4 rows
        
        frame_x = int(self.current_frame) * frame_width
        frame_y = row * frame_height
        
        frame = self.sprite_sheet.subsurface(
            pygame.Rect(frame_x, frame_y, frame_width, frame_height)
        )
        return frame
    
    def update_animation(self, dt):
        """Update animation frame"""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % 4
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw entity on screen"""
        if self.sprite_sheet:
            frame = self.get_current_frame(0)  # Default to first row
            if frame:
                screen.blit(frame, (self.x - camera_x, self.y - camera_y))
        else:
            # Draw colored rectangle as fallback
            pygame.draw.rect(
                screen,
                (255, 0, 255),
                (self.x - camera_x, self.y - camera_y, self.width, self.height)
            )
