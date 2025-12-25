from roguelike.data.definitions import RECIPES, ITEMS
from roguelike.config import COLOR_GREEN, COLOR_RED

def get_item_def(item_id):
    for item in ITEMS:
        if item["id"] == item_id:
            return item
    return None

def craft_item(recipe_index, inventory, game):
    if recipe_index < 0 or recipe_index >= len(RECIPES):
        return

    recipe = RECIPES[recipe_index]

    # Check ingredients
    can_craft = True
    missing = []

    # Count inventory items
    inv_counts = {}
    for item in inventory.items:
        iid = item.item.definition["id"]
        inv_counts[iid] = inv_counts.get(iid, 0) + 1

    for ing, count in recipe["ingredients"].items():
        if inv_counts.get(ing, 0) < count:
            can_craft = False
            missing.append(f"{ing} ({inv_counts.get(ing, 0)}/{count})")

    if can_craft:
        # Remove ingredients
        for ing, count in recipe["ingredients"].items():
            removed = 0
            # Iterate backwards to remove safely
            for i in range(len(inventory.items) - 1, -1, -1):
                if removed >= count: break
                item = inventory.items[i]
                if item.item.definition["id"] == ing:
                    inventory.items.pop(i)
                    removed += 1

        # Add result
        from roguelike.entities import Entity, Item, Equipment
        result_def = get_item_def(recipe["result"])

        # Create Entity (simplified, usually we clone a prototype)
        # We need a way to spawn an item in inventory directly
        # But our Entity system assumes x/y. We'll create it at 0,0 then add to inventory.

        new_item = Entity(0, 0, result_def["name"], result_def["sprite"], blocks=False)
        new_item.item = Item()
        new_item.item.definition = result_def

        if result_def["type"] in ["weapon", "armor"]:
            slot = "main_hand" if result_def["type"] == "weapon" else "body"
            eq = Equipment(slot=slot)
            if result_def.get("power"): eq.power_bonus = result_def["power"]
            if result_def.get("defense"): eq.defense_bonus = result_def["defense"]
            new_item.equipment = eq

        inventory.add_item(new_item)
        game.add_message(f"Crafted {result_def['name']}!", COLOR_GREEN)
        return True
    else:
        game.add_message(f"Missing ingredients: {', '.join(missing)}", COLOR_RED)
        return False
