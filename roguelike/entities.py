import math

class Entity:
    def __init__(self, x, y, name, sprite_name, blocks=False, render_order=1):
        self.x = x
        self.y = y
        self.name = name
        self.sprite_name = sprite_name
        self.blocks = blocks
        self.render_order = render_order

        # Components
        self.fighter = None
        self.ai = None
        self.inventory = None
        self.item = None
        self.equipment = None

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def distance_to(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.stamina = 10
        self.max_stamina = 10
        self.xp = 10 # Default XP

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class AI:
    def take_turn(self, target, game_map, game_entities):
        raise NotImplementedError()

class BasicMonster(AI):
    def take_turn(self, target, game_map, game_entities):
        # A* or simple move towards logic will go here
        pass

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def remove_item(self, item):
        self.items.remove(item)

class Item:
    def __init__(self, use_function=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs

class Equipment:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.equipped = False

    def toggle_equip(self, owner):
        if self.equipped:
            self.unequip(owner)
        else:
            self.equip(owner)

    def equip(self, owner):
        self.equipped = True
        # Bonus application logic handled in Fighter or Game update

    def unequip(self, owner):
        self.equipped = False
