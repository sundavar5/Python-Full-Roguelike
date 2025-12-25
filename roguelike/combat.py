from roguelike.config import COLOR_RED, COLOR_WHITE, COLOR_GREEN

def get_attack_cost(attack_type):
    if attack_type == "quick": return 2
    if attack_type == "heavy": return 5
    return 3

def perform_attack(attacker, target, game, attack_type="normal"):
    if not target.fighter:
        return

    # Check Stamina
    cost = get_attack_cost(attack_type)
    if attacker.fighter.stamina < cost:
        game.add_message(f"{attacker.name} is too tired to attack!", COLOR_RED)
        return

    attacker.fighter.stamina -= cost

    # Calculate Damage
    base_damage = attacker.fighter.power

    # Equipment Bonuses
    if attacker.inventory:
        for item in attacker.inventory.items:
            if item.equipment and item.equipment.equipped:
                base_damage += item.equipment.power_bonus

    # Attack Type Modifiers
    multiplier = 1.0
    if attack_type == "quick":
        multiplier = 0.7
    elif attack_type == "heavy":
        multiplier = 1.5

    # Target Defense Bonuses
    defense = target.fighter.defense
    if target.inventory:
        for item in target.inventory.items:
            if item.equipment and item.equipment.equipped:
                defense += item.equipment.defense_bonus

    damage = int((base_damage * multiplier) - defense)

    # Parry/Guard Check (Simplified)
    # If target is guarding (we need to add a state to fighter or entity for this)
    # For now, let's assume if they have a 'guarding' flag
    if getattr(target, 'guarding', False):
        damage = int(damage * 0.5)
        game.add_message(f"{target.name} guards against the blow!", (200, 200, 255))
        target.guarding = False # Reset guard after hit
        target.fighter.stamina = max(0, target.fighter.stamina - 2) # Guard costs stamina on hit

    if damage > 0:
        target.fighter.take_damage(damage)
        game.add_message(f"{attacker.name} hits {target.name} ({attack_type}) for {damage} damage!", COLOR_WHITE)

        if target.fighter.hp <= 0:
            kill_entity(attacker, target, game)
    else:
        game.add_message(f"{attacker.name} attacks {target.name} but does no damage.", COLOR_WHITE)

from roguelike.data.definitions import ITEMS
from roguelike.entities import Entity, Item, Equipment
import random

def kill_entity(attacker, target, game):
    game.add_message(f"{target.name} is dead!", COLOR_RED)
    game.add_message(f"XP gained: {target.fighter.xp}", (255, 215, 0)) # Assuming XP is in fighter or we add it

    # Loot drop
    # 30% chance to drop an item
    if random.random() < 0.3:
        # Pick random item from definitions
        # In a real game, this would be based on monster loot tables
        item_def = random.choice(ITEMS)
        item = Entity(target.x, target.y, item_def["name"], item_def["sprite"], blocks=False, render_order=0)
        item.item = Item()
        item.item.definition = item_def

        if item_def["type"] in ["weapon", "armor"]:
            slot = "main_hand" if item_def["type"] == "weapon" else "body"
            eq = Equipment(slot=slot)
            if item_def.get("power"): eq.power_bonus = item_def["power"]
            if item_def.get("defense"): eq.defense_bonus = item_def["defense"]
            item.equipment = eq

        game.entities.append(item)
        game.add_message(f"{target.name} dropped {item_def['name']}!", (255, 215, 0))

    target.blocks = False
    target.fighter = None
    target.ai = None
    target.name = f"Remains of {target.name}"
    target.sprite_name = "remains" # Fallback handled in render
    target.render_order = 0

def handle_player_move(dx, dy, game):
    dest_x = game.player.x + dx
    dest_y = game.player.y + dy

    # Reset guard if moving
    game.player.guarding = False

    if not game.game_map.is_blocked(dest_x, dest_y):
        target = game.get_blocking_entities(dest_x, dest_y)
        if target:
            # Bump attack (default quick/normal)
            perform_attack(game.player, target, game, "normal")
        else:
            game.player.move(dx, dy)
            game.fov_recompute = True
        return True # Turn taken

    return False # Turn not taken (blocked by wall)

def wait_turn(game):
    # Regen stamina
    if game.player.fighter.stamina < game.player.fighter.max_stamina:
        game.player.fighter.stamina += 1

    if game.player.fighter.hp < game.player.fighter.max_hp:
        game.player.fighter.heal(1)

    game.player.guarding = False # Reset guard
    return True

def toggle_guard(game):
    game.player.guarding = True
    game.add_message("You raise your guard.", COLOR_GREEN)
    return True # Takes a turn
