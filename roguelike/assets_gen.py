import pygame
import os

# Initialize Pygame just for surface creation
pygame.init()

ASSETS_DIR = os.path.join("roguelike", "assets")
TILE_SIZE = 32

COLORS = {
    "transparent": (0, 0, 0, 0),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "grey": (100, 100, 100),
    "dark_grey": (50, 50, 50),
    "floor": (20, 20, 30),
    "wall": (60, 60, 80),
    "grass": (30, 80, 30),
    "water": (20, 40, 100),
    "lava": (150, 40, 10),
    "player": (200, 200, 255),
    "orc": (50, 150, 50),
    "goblin": (100, 200, 100),
    "skeleton": (200, 200, 200),
    "boss": (150, 0, 0),
    "wood": (139, 69, 19),
    "metal": (192, 192, 192),
    "gold": (255, 215, 0),
    "potion_health": (255, 50, 50),
    "scroll": (240, 230, 200),
}

def create_surface(size=(TILE_SIZE, TILE_SIZE)):
    s = pygame.Surface(size, pygame.SRCALPHA)
    return s

def save_surface(surface, name):
    pygame.image.save(surface, os.path.join(ASSETS_DIR, f"{name}.png"))
    print(f"Generated {name}.png")

def gen_tile(name, color, char=None):
    s = create_surface()
    s.fill(color)
    # Add some texture noise
    for _ in range(10):
        x = int(pygame.math.Vector2().x + (pygame.time.get_ticks() % TILE_SIZE)) # Dummy random
        # Just use basic shapes for noise
        rect = pygame.Rect(
            (id(name) * 7 + _ * 13) % TILE_SIZE,
            (id(name) * 11 + _ * 17) % TILE_SIZE,
            2, 2
        )
        pygame.draw.rect(s, (min(color[0]+20, 255), min(color[1]+20, 255), min(color[2]+20, 255)), rect)

    if char:
        # We don't want text, but I'll add a border to distinguish
        pygame.draw.rect(s, (0,0,0), (0,0,TILE_SIZE,TILE_SIZE), 1)

    save_surface(s, name)

def gen_entity(name, color, shape="rect"):
    s = create_surface()
    # Body
    if shape == "rect":
        pygame.draw.rect(s, color, (4, 4, 24, 24))
        pygame.draw.rect(s, (0,0,0), (4, 4, 24, 24), 1)
        # Eyes
        pygame.draw.rect(s, (255,255,255), (8, 8, 4, 4))
        pygame.draw.rect(s, (255,255,255), (20, 8, 4, 4))
    elif shape == "circle":
        pygame.draw.circle(s, color, (16, 16), 12)
        pygame.draw.circle(s, (0,0,0), (16, 16), 12, 1)
        # Eyes
        pygame.draw.circle(s, (255,255,255), (12, 12), 2)
        pygame.draw.circle(s, (255,255,255), (20, 12), 2)

    save_surface(s, name)

def gen_item(name, color, shape="sword"):
    s = create_surface()
    if shape == "sword":
        # Hilt
        pygame.draw.line(s, COLORS["wood"], (8, 24), (12, 20), 3)
        # Crossguard
        pygame.draw.line(s, COLORS["grey"], (8, 20), (16, 28), 3)
        # Blade
        pygame.draw.line(s, color, (12, 20), (24, 8), 3)
    elif shape == "potion":
        pygame.draw.circle(s, color, (16, 20), 8)
        pygame.draw.rect(s, (200,200,200), (14, 8, 4, 6))
    elif shape == "scroll":
        pygame.draw.rect(s, color, (8, 8, 16, 16))
        pygame.draw.line(s, (0,0,0), (10, 12), (22, 12), 1)
        pygame.draw.line(s, (0,0,0), (10, 16), (22, 16), 1)
    elif shape == "material":
        pygame.draw.circle(s, color, (16, 16), 6)

    save_surface(s, name)

def main():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

    # Tiles
    gen_tile("floor", COLORS["floor"])
    gen_tile("wall", COLORS["wall"])
    gen_tile("grass", COLORS["grass"])
    gen_tile("water", COLORS["water"])
    gen_tile("lava", COLORS["lava"])

    # Doors
    s = create_surface()
    s.fill(COLORS["floor"])
    pygame.draw.rect(s, COLORS["wood"], (4, 4, 24, 24))
    pygame.draw.circle(s, (255, 215, 0), (22, 16), 2) # Knob
    save_surface(s, "door_closed")

    s = create_surface()
    s.fill(COLORS["floor"])
    pygame.draw.rect(s, COLORS["wood"], (4, 4, 8, 24)) # Open door look
    save_surface(s, "door_open")

    # Traps
    s = create_surface()
    s.fill(COLORS["floor"])
    pygame.draw.rect(s, (100, 100, 100), (8, 8, 16, 16), 1)
    pygame.draw.line(s, (100, 100, 100), (16, 8), (16, 24), 1)
    pygame.draw.line(s, (100, 100, 100), (8, 16), (24, 16), 1)
    save_surface(s, "trap_triggered")

    # Stairs
    s = create_surface()
    s.fill(COLORS["floor"])
    pygame.draw.rect(s, COLORS["grey"], (8, 8, 16, 16))
    for i in range(4):
        pygame.draw.line(s, (0,0,0), (8, 8+i*4), (24, 8+i*4), 1)
    save_surface(s, "stairs_down")

    # Entities
    gen_entity("player", COLORS["player"], "rect")
    gen_entity("orc", COLORS["orc"], "rect")
    gen_entity("goblin", COLORS["goblin"], "circle")
    gen_entity("skeleton", COLORS["skeleton"], "rect")
    gen_entity("boss", COLORS["boss"], "rect")

    # Items
    gen_item("sword", COLORS["metal"], "sword")
    gen_item("potion_health", COLORS["potion_health"], "potion")
    gen_item("scroll_lightning", COLORS["scroll"], "scroll")
    gen_item("scroll_fireball", (255, 200, 200), "scroll")
    gen_item("scroll_confusion", (200, 200, 255), "scroll")

    # Materials
    gen_item("material_wood", COLORS["wood"], "material")
    gen_item("material_metal", COLORS["metal"], "material")

    # Remains
    s = create_surface()
    pygame.draw.circle(s, (200, 200, 200), (12, 12), 4) # Skull
    pygame.draw.line(s, (200, 200, 200), (16, 20), (24, 28), 2) # Bone
    pygame.draw.line(s, (200, 200, 200), (24, 20), (16, 28), 2) # Bone
    save_surface(s, "remains")

    print("Assets generated.")

if __name__ == "__main__":
    main()
