from roguelike.config import COLOR_GREEN, COLOR_RED, STATE_PLAYING, STATE_INVENTORY
# from roguelike.combat import perform_attack # Unused here currently

def use_item(item_entity, game):
    if item_entity.item.use_function:
        # Special logic for function calls if we implemented them
        pass
    else:
        # Default behavior based on type
        item_def = item_entity.item.definition
        if item_def["type"] == "potion":
             if item_def["effect"] == "healing":
                 if game.player.fighter.hp == game.player.fighter.max_hp:
                     game.add_message("You are already at full health.", COLOR_RED)
                     return
                 game.player.fighter.heal(item_def["amount"])
                 game.add_message(f"You consume the {item_def['name']} and heal {item_def['amount']} HP.", COLOR_GREEN)
                 game.player.inventory.remove_item(item_entity)
        elif item_def["type"] == "weapon" or item_def["type"] == "armor":
             # Equip/Unequip
             if item_entity.equipment:
                 item_entity.equipment.toggle_equip(game.player)
                 status = "equipped" if item_entity.equipment.equipped else "unequipped"
                 game.add_message(f"You {status} the {item_def['name']}.", COLOR_GREEN)
        elif item_def["type"] == "scroll":
             game.add_message(f"Select a target for {item_def['name']} (Left Click or WASD+Enter).", COLOR_GREEN)
             # Logic for targeting requires game state change handled in main/ui
             # Here we just flag the intent.
             # For this iteration, we will implement a simple 'closest enemy' or 'self' logic
             # OR strictly require the player to be in targeting mode first.
             # BETTER: Set game state to targeting, and store the item to be used.
             from roguelike.config import STATE_TARGETING
             game.state = STATE_TARGETING
             game.pending_item = item_entity
             game.add_message("Use arrow keys to select target, Enter to fire.", COLOR_GREEN)

def cast_scroll(item_entity, target_x, target_y, game):
    item_def = item_entity.item.definition
    effect = item_def["effect"]

    # Check LoS
    # (Assuming we have a function or we just trust the target selection)

    if effect == "fireball":
        # Area damage
        game.add_message(f"A fireball explodes at ({target_x}, {target_y})!", COLOR_RED)
        for entity in game.entities:
            if entity.fighter and entity.distance_to(type('obj', (object,), {'x': target_x, 'y': target_y})) <= 2:
                entity.fighter.take_damage(10)
                game.add_message(f"{entity.name} takes 10 fire damage!", COLOR_RED)
                if entity.fighter.hp <= 0:
                    # Circular import avoidance for kill_entity?
                    # Ideally kill_entity should be in a shared util or game method.
                    # For now, we will handle death in next update loop or call combat.kill_entity inside game?
                    # We'll just set hp to 0 and let game loop clean up or import locally.
                    from roguelike.combat import kill_entity
                    kill_entity(game.player, entity, game)

    elif effect == "lightning":
        # Single target high damage
        target = game.get_blocking_entities(target_x, target_y)
        if target and target.fighter:
            target.fighter.take_damage(20)
            game.add_message(f"Lightning strikes {target.name} for 20 damage!", COLOR_RED)
            if target.fighter.hp <= 0:
                from roguelike.combat import kill_entity
                kill_entity(game.player, target, game)
        else:
             game.add_message("The lightning hits the ground.", COLOR_WHITE)

    elif effect == "confusion":
        target = game.get_blocking_entities(target_x, target_y)
        if target and target.ai:
             # Placeholder for confusion status
             game.add_message(f"{target.name} looks confused!", COLOR_GREEN)

    game.player.inventory.remove_item(item_entity)

def drop_item(item_entity, game):
    game.player.inventory.remove_item(item_entity)
    item_entity.x = game.player.x
    item_entity.y = game.player.y
    game.entities.append(item_entity)
    game.add_message(f"You dropped the {item_entity.name}.", COLOR_GREEN)

def pickup_item(game):
    item_to_pickup = None
    for entity in game.entities:
        if entity.item and entity.x == game.player.x and entity.y == game.player.y:
            item_to_pickup = entity
            break

    if item_to_pickup:
        if game.player.inventory.add_item(item_to_pickup):
            game.entities.remove(item_to_pickup)
            game.add_message(f"You picked up {item_to_pickup.name}.", COLOR_GREEN)
        else:
            game.add_message("Inventory is full.", COLOR_RED)
    else:
        game.add_message("There is nothing here to pick up.", COLOR_RED)
