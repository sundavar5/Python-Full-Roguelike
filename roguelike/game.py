from roguelike.config import *
from roguelike.entities import Entity, Fighter, Inventory
from roguelike.worldgen import GameMap
from roguelike.data.definitions import BASE_STATS

class Game:
    def __init__(self):
        self.state = STATE_MAIN_MENU
        self.map_width = MAP_WIDTH
        self.map_height = MAP_HEIGHT
        self.game_map = None
        self.player = None
        self.entities = []
        self.message_log = []
        self.fov_recompute = True
        self.fov_map = None # Should be computed in render/fov module, but logic state here

        # Targeting state
        self.target_x = 0
        self.target_y = 0
        self.pending_item = None

    def new_game(self):
        self.entities = []
        # Create Player
        self.player = Entity(0, 0, "Player", "player", blocks=True, render_order=3)
        self.player.fighter = Fighter(hp=BASE_STATS["hp"] * 3, defense=1, power=4, dexterity=15, intelligence=12, strength=14, constitution=14)
        self.player.inventory = Inventory(capacity=26)
        self.entities.append(self.player)

        # Generate Map
        self.game_map = GameMap(self.map_width, self.map_height)
        self.game_map.make_map(30, 6, 10, self.map_width, self.map_height, self.player, self.entities)

        self.state = STATE_PLAYING
        self.add_message("Welcome to the Dungeon!", COLOR_RED)

    def add_message(self, text, color=COLOR_WHITE):
        self.message_log.append((text, color))
        if len(self.message_log) > 50:
            self.message_log.pop(0)

    def get_blocking_entities(self, x, y):
        for entity in self.entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return entity
        return None

    def next_level(self):
        self.add_message("You take a moment to rest, and recover your strength.", (100, 255, 100))
        self.player.fighter.heal(self.player.fighter.max_hp // 2)

        self.add_message("You descend deeper into the heart of the dungeon...", COLOR_RED)

        # Keep player but clear other entities
        self.entities = [self.player]

        # Generate new map (harder? not implemented difficulty scaling yet)
        self.game_map = GameMap(self.map_width, self.map_height)
        self.game_map.make_map(30, 6, 10, self.map_width, self.map_height, self.player, self.entities)

        self.fov_recompute = True

    def update_effects(self):
        for entity in self.entities:
            if hasattr(entity, 'status_effects'):
                to_remove = []
                for effect in entity.status_effects:
                    if effect.tick(entity, self):
                        to_remove.append(effect)

                for effect in to_remove:
                    effect.remove(entity, self)
                    entity.status_effects.remove(effect)
