from roguelike.config import COLOR_GREEN, COLOR_RED, STATE_PLAYING
from roguelike.data.definitions import RECIPES

def dismantle_item(item_entity, game):
    # Determine materials to return
    # If item is crafted, return 50% of ingredients?
    # Or just generic based on type

    item_def = item_entity.item.definition

    # Only dismantle weapons/armor
    if item_def["type"] not in ["weapon", "armor"]:
         game.add_message("You cannot dismantle that.", COLOR_RED)
         return False

    mat_name = item_def["id"].split("_")[0]
    # Handle "material_wood" vs just "wood" prefix
    if "material_" not in mat_name:
        # Check standard materials list or infer
        # Definitions.py uses "wood_sword" -> mat "wood" -> item "material_wood"
        pass

    # Give 1 material
    # Check if material entity exists in definitions to spawn it
    mat_id = f"material_{mat_name}"

    # Helper to find def
    from roguelike.data.definitions import ITEMS
    mat_def = next((i for i in ITEMS if i["id"] == mat_id), None)

    if mat_def:
        # Add to inventory
        from roguelike.entities import Entity, Item
        mat_ent = Entity(0, 0, mat_def["name"], mat_def["sprite"], blocks=False)
        mat_ent.item = Item()
        mat_ent.item.definition = mat_def

        if game.player.inventory.add_item(mat_ent):
            game.player.inventory.remove_item(item_entity)
            game.add_message(f"You dismantle the {item_def['name']} into {mat_def['name']}.", COLOR_GREEN)
            return True
        else:
             game.add_message("Inventory full.", COLOR_RED)
             return False
    else:
        # Fallback
        game.add_message("You salvage nothing useful.", COLOR_RED)
        game.player.inventory.remove_item(item_entity)
        return True
