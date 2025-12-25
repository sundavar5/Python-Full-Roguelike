import random
from roguelike.entities import Entity, Fighter, AI, BasicMonster, Item, Inventory, Equipment
from roguelike.config import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from roguelike.data.definitions import ENEMIES, ITEMS

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
        self.explored = False
        self.sprite = "wall" if blocked else "floor"

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.entities = []

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
                self.tiles[x][y].sprite = "floor"

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            self.tiles[x][y].sprite = "floor"

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            self.tiles[x][y].sprite = "floor"

    def place_entities(self, room, entities):
        # Generate max monsters per room
        number_of_monsters = random.randint(0, 3)
        number_of_items = random.randint(0, 2)

        for i in range(number_of_monsters):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # Choose random monster
                monster_def = random.choice(ENEMIES)
                monster = Entity(x, y, monster_def["name"], monster_def["color"], blocks=True, render_order=2)
                fighter = Fighter(hp=monster_def["hp"], defense=monster_def["defense"], power=monster_def["power"])
                ai = BasicMonster()
                monster.fighter = fighter
                monster.ai = ai
                entities.append(monster)

        for i in range(number_of_items):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_def = random.choice(ITEMS)
                item = Entity(x, y, item_def["name"], item_def["sprite"], blocks=False, render_order=0)
                item.item = Item()
                item.item.definition = item_def

                # Check for Equipment
                if item_def["type"] in ["weapon", "armor"]:
                    slot = "main_hand" if item_def["type"] == "weapon" else "body"
                    eq = Equipment(slot=slot)
                    if item_def.get("power"): eq.power_bonus = item_def["power"]
                    if item_def.get("defense"): eq.defense_bonus = item_def["defense"]
                    item.equipment = eq

                entities.append(item)

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)
            x = random.randint(0, map_width - w - 1)
            y = random.randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if random.randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1

        # Place Stairs in the last room
        last_room = rooms[-1]
        sx, sy = last_room.center()
        stairs = Entity(sx, sy, "Stairs", "stairs_down", render_order=0)
        entities.append(stairs)
        self.stairs = stairs
