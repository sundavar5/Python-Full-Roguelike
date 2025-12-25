import random
import os

LORE_FILE = "roguelike/data/massive_lore.py"
ITEMS_FILE = "roguelike/data/massive_items.py"

YEAR_START = 100
YEAR_END = 5000
KING_NAMES = ["Arthur", "Belgarath", "Crom", "Darius", "Erebus", "Fandor", "Grom", "Hrothgar", "Isildur", "Jareth"]
PLACES = ["the North", "the South", "the Void", "Shadows", "Light", "Iron", "Gold", "Bone", "Mist", "Fire"]
ACTIONS = ["conquered", "destroyed", "built", "discovered", "lost", "forged", "cursed", "blessed", "ate", "burned"]
OBJECTS = ["Crown", "Scepter", "Sword", "Shield", "Ring", "Amulet", "Gem", "Tome", "Scroll", "Orb"]

def generate_lore():
    print(f"Generating {LORE_FILE}...")
    with open(LORE_FILE, "w") as f:
        f.write("# Massive generated lore library\n\n")
        f.write("MASSIVE_LORE = [\n")

        for i in range(10000):
            year = random.randint(YEAR_START, YEAR_END)
            king = random.choice(KING_NAMES)
            place = random.choice(PLACES)
            action = random.choice(ACTIONS)
            obj = random.choice(OBJECTS)

            text = f"In the year {year}, King {king} of {place} {action} the {obj} of {random.choice(PLACES)}."
            # Add some padding to ensure lines are distinct and reasonably long
            text += f" This event is recorded in the archives as Entry #{i+1}, signifying a turning point in the Age of {random.choice(PLACES)}."

            f.write(f"    {{\n")
            f.write(f"        'id': {i + 1000},\n")
            f.write(f"        'year': {year},\n")
            f.write(f"        'title': 'The Legend of {king}',\n")
            f.write(f"        'text': \"{text}\"\n")
            f.write(f"    }},\n")

        f.write("]\n")
    print("Lore generated.")

def generate_items():
    print(f"Generating {ITEMS_FILE}...")
    with open(ITEMS_FILE, "w") as f:
        f.write("# Massive generated unique items\n\n")
        f.write("MASSIVE_ITEMS = [\n")

        for i in range(5000):
            king = random.choice(KING_NAMES)
            obj = random.choice(OBJECTS)
            place = random.choice(PLACES)

            name = f"{king}'s {obj} of {place}"
            item_id = f"unique_{obj.lower()}_{i}"

            # Random stats
            power = random.randint(5, 50)
            value = random.randint(100, 1000)

            f.write(f"    {{\n")
            f.write(f"        'id': '{item_id}',\n")
            f.write(f"        'name': \"{name}\",\n")
            f.write(f"        'type': 'weapon',\n") # Simplified type
            f.write(f"        'sprite': 'sword',\n")
            f.write(f"        'power': {power},\n")
            f.write(f"        'weight': {random.randint(1, 10)},\n")
            f.write(f"        'value': {value},\n")
            f.write(f"        'description': \"A legendary item forged in the fires of {place}.\"\n")
            f.write(f"    }},\n")

        f.write("]\n")
    print("Items generated.")

if __name__ == "__main__":
    generate_lore()
    generate_items()
