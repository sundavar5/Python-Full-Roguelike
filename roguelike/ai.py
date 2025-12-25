from roguelike.combat import perform_attack
from roguelike.ai_states import AdvancedMonster
from roguelike.status import Stun
import random

def basic_monster_turn(monster, target, game):
    # Check for Stun
    for effect in monster.status_effects:
        if isinstance(effect, Stun):
            return

    # Fleeing Logic (Overrides standard behavior if critical health)
    if monster.fighter.hp < monster.fighter.max_hp * 0.2:
        if monster.ai and not isinstance(monster.ai, FleeingMonster):
             # Switch AI to fleeing? Or just execute fleeing logic here?
             # Swapping AI is cleaner for persistent state
             monster.ai = FleeingMonster()
             monster.ai.take_turn(monster, target, game)
             return

    if monster.distance_to(target) >= 2:
        # Move towards player
        dx = target.x - monster.x
        dy = target.y - monster.y

        distance = (dx ** 2 + dy ** 2) ** 0.5
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not game.game_map.is_blocked(monster.x + dx, monster.y + dy):
             if not game.get_blocking_entities(monster.x + dx, monster.y + dy):
                 monster.move(dx, dy)
    elif target.fighter.hp > 0:
        perform_attack(monster, target, game, "normal")

def enemy_turn(game):
    for entity in game.entities:
        if entity.ai:
            if isinstance(entity.ai, AdvancedMonster):
                 entity.ai.take_turn(entity, game)
            elif hasattr(entity.ai, "take_turn"):
                # New AI class based
                entity.ai.take_turn(entity, game.player, game)
            else:
                # Fallback
                basic_monster_turn(entity, game.player, game)

# New AI Classes

class ConfusedMonster:
    def __init__(self, old_ai=None, num_turns=10):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self, monster, target, game):
        if self.num_turns > 0:
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
            if dx != 0 or dy != 0:
                 if not game.game_map.is_blocked(monster.x + dx, monster.y + dy):
                     if not game.get_blocking_entities(monster.x + dx, monster.y + dy):
                         monster.move(dx, dy)
            self.num_turns -= 1
        else:
            monster.ai = self.old_ai
            game.add_message(f"The {monster.name} is no longer confused!", (255, 0, 0))

class FleeingMonster:
    def take_turn(self, monster, target, game):
        # Move AWAY from player
        dx = monster.x - target.x
        dy = monster.y - target.y

        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))

            new_x = monster.x + dx
            new_y = monster.y + dy

            if not game.game_map.is_blocked(new_x, new_y):
                if not game.get_blocking_entities(new_x, new_y):
                    monster.move(dx, dy)
                    game.add_message(f"{monster.name} flees in terror!", (255, 200, 200))
                    return

        # If cornered or far enough?
        # Maybe attack if cornered
        if distance < 2 and target.fighter.hp > 0:
             perform_attack(monster, target, game, "quick")


class RangedMonster:
    def take_turn(self, monster, target, game):
        dist = monster.distance_to(target)

        # Maintain distance 3-5
        if dist < 3:
             # Too close, back away
             dx = monster.x - target.x
             dy = monster.y - target.y
             distance_val = (dx ** 2 + dy ** 2) ** 0.5
             if distance_val > 0:
                dx = int(round(dx / distance_val))
                dy = int(round(dy / distance_val))
                if not game.game_map.is_blocked(monster.x + dx, monster.y + dy) and not game.get_blocking_entities(monster.x + dx, monster.y + dy):
                    monster.move(dx, dy)
                    return # Moved, so turn done

        elif dist > 5:
             # Too far, move closer
             dx = target.x - monster.x
             dy = target.y - monster.y
             distance_val = (dx ** 2 + dy ** 2) ** 0.5
             if distance_val > 0:
                dx = int(round(dx / distance_val))
                dy = int(round(dy / distance_val))
                if not game.game_map.is_blocked(monster.x + dx, monster.y + dy) and not game.get_blocking_entities(monster.x + dx, monster.y + dy):
                    monster.move(dx, dy)
                    return

        # Attack if in range
        if dist <= 6 and target.fighter.hp > 0:
             # Basic LoS check (omitted for brevity, assuming clear shot if in room)
             game.add_message(f"{monster.name} shoots at {target.name}!", (255, 100, 0))
             perform_attack(monster, target, game, "normal")
