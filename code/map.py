import pygame
import pytmx
from code.trainer import Trainer
import random

class Map:
    def __init__(self, tmx_path):
        self.tmx_data = pytmx.load_pygame(tmx_path)
        self.width = self.tmx_data.width
        self.height = self.tmx_data.height
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        
        print(f"Map size: {self.width}x{self.height} tiles ({self.tile_width}x{self.tile_height} px per tile)")
        
        # Load collision and grass tiles
        self.collision_tiles = self.load_layer_tiles("collisions")
        self.grass_tiles = self.load_layer_tiles("grass")
        self.lottery_tiles = self.load_layer_tiles("house_lottery")
        
        print(f"Total collision tiles: {len(self.collision_tiles)}")
        print(f"Total grass tiles: {len(self.grass_tiles)}")
        print(f"Total lottery tiles: {len(self.lottery_tiles)}")
        
        # Spawn trainers
        self.trainers = []
        self.spawn_trainers()
    
    def load_layer_tiles(self, layer_name):
        """Load all tile positions from object layers or tile layers"""
        tiles = set()
        
        # Try to find as a direct object layer
        try:
            layer = self.tmx_data.get_layer_by_name(layer_name)
            
            if isinstance(layer, pytmx.TiledObjectGroup):
                # It's an object layer - process all objects in it
                for obj in layer:
                    # Calculate tile positions covered by this object
                    start_x = int(obj.x // self.tile_width)
                    start_y = int(obj.y // self.tile_height)
                    end_x = int((obj.x + obj.width) // self.tile_width)
                    end_y = int((obj.y + obj.height) // self.tile_height)
                    
                    # Add all tiles covered by this object
                    for tx in range(start_x, end_x):
                        for ty in range(start_y, end_y):
                            tiles.add((tx, ty))
                
                print(f"Loaded {len(tiles)} tiles from object layer '{layer_name}'")
                return tiles
            
            elif isinstance(layer, pytmx.TiledTileLayer):
                # It's a tile layer
                count = 0
                for x, y, gid in layer:
                    if gid != 0:
                        tiles.add((x, y))
                        count += 1
                if count > 0:
                    print(f"Loaded {count} tiles from tile layer '{layer_name}'")
                return tiles
        except ValueError:
            pass
        except Exception as e:
            print(f"Error loading layer '{layer_name}': {e}")
        
        # If not found as direct layer, try looking in interface object group
        try:
            interface_layer = self.tmx_data.get_layer_by_name("interface")
            
            if isinstance(interface_layer, pytmx.TiledObjectGroup):
                for obj in interface_layer:
                    obj_identifier = obj.name or obj.type or ""
                    
                    if layer_name.lower() in obj_identifier.lower():
                        start_x = int(obj.x // self.tile_width)
                        start_y = int(obj.y // self.tile_height)
                        end_x = int((obj.x + obj.width) // self.tile_width)
                        end_y = int((obj.y + obj.height) // self.tile_height)
                        
                        for tx in range(start_x, end_x):
                            for ty in range(start_y, end_y):
                                tiles.add((tx, ty))
                        
                        print(f"Loaded {len(tiles)} tiles for '{layer_name}' from interface object '{obj_identifier}'")
                        return tiles
        except ValueError:
            pass
        except Exception as e:
            print(f"Error loading from interface layer: {e}")
        
        if len(tiles) == 0:
            print(f"Warning: No tiles found for '{layer_name}'")
        
        return tiles
    
    def spawn_trainers(self):
        """Spawn trainers at random valid positions"""
        num_trainers = 15
        for _ in range(num_trainers):
            # Find random valid position
            attempts = 0
            while attempts < 100:
                x = random.randint(5, self.width - 5) * self.tile_width
                y = random.randint(5, self.height - 5) * self.tile_height
                
                tile_x = x // self.tile_width
                tile_y = y // self.tile_height
                
                if (tile_x, tile_y) not in self.collision_tiles:
                    trainer = Trainer(x, y)
                    self.trainers.append(trainer)
                    break
                attempts += 1
    
    def draw(self, screen, camera_x, camera_y):
        """Draw all visible layers"""
        # Draw all layers except collision/grass markers
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name in ["collisions", "grass", "house_lottery"]:
                    continue
                
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen_x = x * self.tile_width - camera_x
                        screen_y = y * self.tile_height - camera_y
                        screen.blit(tile, (screen_x, screen_y))
        
        # Draw trainers
        for trainer in self.trainers:
            if trainer.visible:
                trainer.draw(screen, camera_x, camera_y)
    
    def is_collision(self, x, y, width, height):
        """Check if a rectangle collides with any collision tiles"""
        # Check corners and center
        points = [
            (x, y),
            (x + width, y),
            (x, y + height),
            (x + width, y + height),
            (x + width // 2, y + height // 2)
        ]
        
        for px, py in points:
            tile_x = int(px // self.tile_width)
            tile_y = int(py // self.tile_height)
            if (tile_x, tile_y) in self.collision_tiles:
                return True
        
        return False
    
    def is_on_grass(self, entity):
        """Check if entity is standing on grass"""
        # Use hitbox for player
        if hasattr(entity, 'hitbox_offset_x'):
            center_x = entity.x + entity.hitbox_offset_x + entity.hitbox_width // 2
            center_y = entity.y + entity.hitbox_offset_y + entity.hitbox_height // 2
        else:
            center_x = entity.x + entity.width // 2
            center_y = entity.y + entity.height // 2
        
        tile_x = int(center_x // self.tile_width)
        tile_y = int(center_y // self.tile_height)
        return (tile_x, tile_y) in self.grass_tiles
    
    def check_trainer_collision(self, player):
        """Check if player is near a trainer"""
        # Use player's hitbox
        player_rect = pygame.Rect(
            player.x + player.hitbox_offset_x,
            player.y + player.hitbox_offset_y,
            player.hitbox_width,
            player.hitbox_height
        )
        
        for trainer in self.trainers:
            if not trainer.visible or trainer.in_battle:
                continue
            
            trainer_rect = pygame.Rect(trainer.x, trainer.y, trainer.width, trainer.height)
            if player_rect.colliderect(trainer_rect):
                return trainer
        
        return None
    
    def check_lottery_collision(self, player):
        """Check if player is on a lottery house tile"""
        # Use player's hitbox center
        center_x = player.x + player.hitbox_offset_x + player.hitbox_width // 2
        center_y = player.y + player.hitbox_offset_y + player.hitbox_height // 2
        
        tile_x = int(center_x // self.tile_width)
        tile_y = int(center_y // self.tile_height)
        return (tile_x, tile_y) in self.lottery_tiles
    
    def update_trainers(self, dt):
        """Update all trainers (respawn timers)"""
        for trainer in self.trainers:
            trainer.update(dt)