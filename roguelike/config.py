import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Python Roguelike"

# Tile settings
TILE_SIZE = 32

# Map settings
MAP_WIDTH = 50
MAP_HEIGHT = 50
FOV_RADIUS = 10

# FPS
FPS = 30

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

# Key Bindings
KEY_MOVE_UP = pygame.K_w
KEY_MOVE_DOWN = pygame.K_s
KEY_MOVE_LEFT = pygame.K_a
KEY_MOVE_RIGHT = pygame.K_d
KEY_WAIT = pygame.K_SPACE
KEY_INVENTORY = pygame.K_i
KEY_PICKUP = pygame.K_g
KEY_DROP = pygame.K_d  # In inventory context
KEY_USE = pygame.K_e
KEY_ESCAPE = pygame.K_ESCAPE
KEY_ENTER = pygame.K_RETURN
KEY_LOOK = pygame.K_k # Reassigned to avoid conflict with Lore
KEY_ATTACK_MODE = pygame.K_f
KEY_GUARD = pygame.K_z
KEY_CRAFTING = pygame.K_c
KEY_RANGED = pygame.K_r
KEY_TARGET = pygame.K_t
KEY_LORE = pygame.K_l
KEY_DISMANTLE = pygame.K_x
KEY_CHARACTER = pygame.K_p
KEY_SKILLS = pygame.K_k

# Game States
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_INVENTORY = 2
STATE_GAME_OVER = 3
STATE_VICTORY = 4
STATE_LOOK = 5
STATE_ATTACK_DIRECTION = 6
STATE_CRAFTING = 7
STATE_TARGETING = 8
STATE_LORE = 9
STATE_LEVEL_UP = 10
STATE_CHARACTER_SCREEN = 11
STATE_SKILLS = 12
