import pygame
import os
from roguelike.config import *

class Renderer:
    def __init__(self, screen, assets_dir):
        self.screen = screen
        self.assets = {}
        self.load_assets(assets_dir)
        self.camera_x = 0
        self.camera_y = 0
        self.visible_tiles = set()
        self.font = pygame.font.Font(None, 24)

    def load_assets(self, assets_dir):
        for filename in os.listdir(assets_dir):
            if filename.endswith(".png"):
                name = filename.split(".")[0]
                img = pygame.image.load(os.path.join(assets_dir, filename)).convert_alpha()
                self.assets[name] = img

    def update_fov(self, game_map, player):
        self.visible_tiles = set()
        # Simple Raycasting or Shadowcasting
        # For simplicity in this timeframe, we use simple distance check
        # But for "Fog of War + line-of-sight shading" we need at least naive raycasting

        radius = FOV_RADIUS
        for x in range(player.x - radius, player.x + radius + 1):
            for y in range(player.y - radius, player.y + radius + 1):
                if 0 <= x < game_map.width and 0 <= y < game_map.height:
                    # Line of Sight check
                    if self.line_of_sight(player.x, player.y, x, y, game_map):
                        self.visible_tiles.add((x, y))
                        game_map.tiles[x][y].explored = True

    def line_of_sight(self, x0, y0, x1, y1, game_map):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        n = 1 + dx + dy
        x_inc = 1 if x1 > x0 else -1
        y_inc = 1 if y1 > y0 else -1
        error = dx - dy
        dx *= 2
        dy *= 2

        for _ in range(n):
            if game_map.tiles[x][y].block_sight and (x, y) != (x1, y1) and (x, y) != (x0, y0):
                return False

            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
        return True

    def render_all(self, game):
        # Center camera on player
        self.camera_x = game.player.x * TILE_SIZE - SCREEN_WIDTH // 2
        self.camera_y = game.player.y * TILE_SIZE - SCREEN_HEIGHT // 2

        self.screen.fill(COLOR_BLACK)

        # Draw Map
        for x in range(game.game_map.width):
            for y in range(game.game_map.height):
                visible = (x, y) in self.visible_tiles
                explored = game.game_map.tiles[x][y].explored

                if visible or explored:
                    tile = game.game_map.tiles[x][y]
                    screen_x = x * TILE_SIZE - self.camera_x
                    screen_y = y * TILE_SIZE - self.camera_y

                    if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
                        if tile.sprite in self.assets:
                            img = self.assets[tile.sprite]
                            if not visible:
                                # Darken explored but not visible tiles
                                img = img.copy()
                                img.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)
                            self.screen.blit(img, (screen_x, screen_y))

        # Draw Entities
        entities_in_render_order = sorted(game.entities, key=lambda x: x.render_order)
        for entity in entities_in_render_order:
            if (entity.x, entity.y) in self.visible_tiles:
                screen_x = entity.x * TILE_SIZE - self.camera_x
                screen_y = entity.y * TILE_SIZE - self.camera_y
                if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
                    if entity.sprite_name in self.assets:
                        self.screen.blit(self.assets[entity.sprite_name], (screen_x, screen_y))
                    else:
                        # Fallback rectangle
                        pygame.draw.rect(self.screen, (255, 0, 255), (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

        # Draw Targeting Cursor
        if game.state == STATE_TARGETING:
             screen_x = game.target_x * TILE_SIZE - self.camera_x
             screen_y = game.target_y * TILE_SIZE - self.camera_y
             pygame.draw.rect(self.screen, COLOR_GREEN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE), 2)
