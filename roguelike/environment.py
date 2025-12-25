from roguelike.entities import Entity, Fighter
from roguelike.config import COLOR_WHITE, COLOR_RED, TILE_SIZE
import random

class Door(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "Door", "door_closed", blocks=True, render_order=1)
        self.is_open = False

    def open(self):
        if not self.is_open:
            self.is_open = True
            self.blocks = False
            self.sprite_name = "door_open"
            self.name = "Open Door"
            # Update opacity/sight blocking?
            # GameMap tile needs to be updated for LoS
            return True
        return False

    def close(self):
        if self.is_open:
            self.is_open = False
            self.blocks = True
            self.sprite_name = "door_closed"
            self.name = "Closed Door"
            return True
        return False

class Trap(Entity):
    def __init__(self, x, y, damage=5):
        super().__init__(x, y, "Trap", "floor", blocks=False, render_order=0)
        self.damage = damage
        self.revealed = False
        self.triggered = False

    def trigger(self, target, game):
        if not self.triggered:
            self.triggered = True
            self.revealed = True
            self.sprite_name = "trap_triggered" # Need asset
            if target.fighter:
                target.fighter.take_damage(self.damage)
                game.add_message(f"{target.name} triggers a trap taking {self.damage} damage!", COLOR_RED)
                from roguelike.status import Poison
                if random.random() < 0.3:
                    target.add_effect(Poison(5, 1), game)
            return True
        return False
