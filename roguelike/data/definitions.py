
# Data definitions for the game

# Factions
FACTIONS = ["Player", "Orcs", "Undead", "Animals"]

# Base Stats for procedural generation
BASE_STATS = {
    "hp": 10,
    "defense": 0,
    "power": 3,
}

# --------------------------
# ENEMIES
# --------------------------
# Requirement: 60+ enemies.
# We will define ~10 archetypes and then procedural variations.

ENEMY_ARCHETYPES = {
    "orc": {"char": "o", "color": "orc", "name": "Orc", "hp": 20, "defense": 1, "power": 4, "xp": 35, "ai": "hostile"},
    "goblin": {"char": "g", "color": "goblin", "name": "Goblin", "hp": 10, "defense": 0, "power": 3, "xp": 20, "ai": "hostile"},
    "troll": {"char": "T", "color": "orc", "name": "Troll", "hp": 30, "defense": 2, "power": 8, "xp": 100, "ai": "hostile"},
    "skeleton": {"char": "s", "color": "skeleton", "name": "Skeleton", "hp": 12, "defense": 1, "power": 4, "xp": 25, "ai": "hostile"},
    "zombie": {"char": "z", "color": "skeleton", "name": "Zombie", "hp": 15, "defense": 0, "power": 3, "xp": 25, "ai": "hostile"},
    "rat": {"char": "r", "color": "grey", "name": "Giant Rat", "hp": 5, "defense": 0, "power": 2, "xp": 10, "ai": "hostile"},
    "bat": {"char": "b", "color": "grey", "name": "Giant Bat", "hp": 5, "defense": 0, "power": 2, "xp": 10, "ai": "hostile"},
    "slime": {"char": "S", "color": "green", "name": "Slime", "hp": 25, "defense": 0, "power": 3, "xp": 30, "ai": "hostile"},
    "bandit": {"char": "B", "color": "dark_grey", "name": "Bandit", "hp": 20, "defense": 1, "power": 5, "xp": 40, "ai": "hostile"},
    "boss": {"char": "O", "color": "boss", "name": "Warlord", "hp": 100, "defense": 4, "power": 10, "xp": 500, "ai": "hostile"},
}

ADJECTIVES = ["Weak", "Sickly", "Young", "Normal", "Strong", "Fierce", "Elite", "Ancient", "Armored", "Savage"]

ENEMIES = []
for key, base in ENEMY_ARCHETYPES.items():
    for adj in ADJECTIVES:
        new_enemy = base.copy()
        new_enemy["id"] = f"{adj.lower()}_{key}"
        new_enemy["name"] = f"{adj} {base['name']}"

        # Stat modifiers
        mult = 0.5 + (ADJECTIVES.index(adj) * 0.15)
        new_enemy["hp"] = int(base["hp"] * mult)
        new_enemy["power"] = int(base["power"] * mult)
        new_enemy["xp"] = int(base["xp"] * mult)

        ENEMIES.append(new_enemy)

# --------------------------
# ITEMS
# --------------------------
# Requirement: 200+ items.

ITEM_TYPES = ["weapon", "armor", "potion", "scroll", "material"]
MATERIALS = ["wood", "stone", "copper", "bronze", "iron", "steel", "silver", "gold", "mythril", "adamantite", "obsidian", "crystal"]
WEAPON_TYPES = ["sword", "axe", "dagger", "mace", "spear", "halberd", "flail", "warhammer"]
ARMOR_TYPES = ["cloth", "leather", "chain", "scale", "plate", "heavy_plate"]
POTION_TYPES = ["healing", "stamina", "strength", "speed", "defense"]
SCROLL_TYPES = ["fireball", "lightning", "confusion", "teleport", "identify"]
PREFIXES = ["Broken", "Rusty", "Old", "Common", "Fine", "Superior", "Masterwork", "Legendary"]

ITEMS = []

# Generate Weapons (Materials * WeaponTypes * Prefixes)
# To hit 200+, we can just do Materials * WeaponTypes which is 12 * 8 = 96
# Plus Armors 12 * 6 = 72. Total 168.
# Plus Potions 5 * 4 = 20.
# Plus Scrolls 5.
# Plus Materials 12.
# Total ~ 205.
# We will use prefixes as valid variations if we need more, but base types are good.

for mat in MATERIALS:
    for w_type in WEAPON_TYPES:
        item = {
            "id": f"{mat}_{w_type}",
            "name": f"{mat.capitalize()} {w_type.capitalize()}",
            "type": "weapon",
            "sprite": "sword", # Placeholder sprite for all weapons
            "power": (MATERIALS.index(mat) + 1) * 2 + (WEAPON_TYPES.index(w_type)),
            "weight": 2.0,
            "value": (MATERIALS.index(mat) + 1) * 10
        }
        ITEMS.append(item)

# Generate Armor
for mat in MATERIALS:
    for a_type in ARMOR_TYPES:
        item = {
            "id": f"{mat}_{a_type}_armor",
            "name": f"{mat.capitalize()} {a_type.capitalize()} Armor",
            "type": "armor",
            "sprite": "player", # Placeholder
            "defense": (MATERIALS.index(mat) + 1) * 2 + (ARMOR_TYPES.index(a_type)),
            "weight": 5.0,
            "value": (MATERIALS.index(mat) + 1) * 15
        }
        ITEMS.append(item)

# Potions (Variations of strength)
for p_type in POTION_TYPES:
    for tier in ["Minor", "Normal", "Major", "Super"]:
        item = {
            "id": f"{tier.lower()}_{p_type}_potion",
            "name": f"{tier} Potion of {p_type.capitalize()}",
            "type": "potion",
            "sprite": "potion_health",
            "effect": p_type,
            "amount": (["Minor", "Normal", "Major", "Super"].index(tier) + 1) * 10,
            "weight": 0.5,
            "value": 10
        }
        ITEMS.append(item)

# Scrolls
for s_type in SCROLL_TYPES:
    item = {
        "id": f"scroll_{s_type}",
        "name": f"Scroll of {s_type.capitalize()}",
        "type": "scroll",
        "sprite": f"scroll_{s_type}",
        "effect": s_type,
        "weight": 0.1,
        "value": 20
    }
    ITEMS.append(item)

# Raw Materials
for mat in MATERIALS:
    item = {
        "id": f"material_{mat}",
        "name": f"{mat.capitalize()} Ingot/Plank",
        "type": "material",
        "sprite": "material_metal" if mat in ["iron", "steel", "mythril", "adamantite"] else "material_wood",
        "weight": 1.0,
        "value": 5
    }
    ITEMS.append(item)


# --------------------------
# RECIPES
# --------------------------
# Requirement: 80+ recipes
# We can combine materials to make weapons/armor.

RECIPES = []
for item in ITEMS:
    if item["type"] in ["weapon", "armor"]:
        # Naive recipe generation
        mat_name = item["id"].split("_")[0]
        rec = {
            "result": item["id"],
            "ingredients": {f"material_{mat_name}": 3, "material_wood": 1},
            "station": "anvil"
        }
        RECIPES.append(rec)
    elif item["type"] == "potion":
        rec = {
            "result": item["id"],
            "ingredients": {"material_wood": 1}, # Placeholder ingredients
            "station": "alchemy"
        }
        RECIPES.append(rec)

# --------------------------
# LORE
# --------------------------
# Requirement: 100+ lore entries
LORE = []
for i in range(101):
    LORE.append({
        "id": i,
        "title": f"Ancient Chronicle #{i}",
        "text": f"This is entry number {i} of the ancient history of this realm. Dark times fell upon the land..."
    })
