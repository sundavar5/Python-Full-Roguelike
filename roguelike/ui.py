import pygame
from roguelike.config import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 40)

    def draw_bar(self, x, y, current, maximum, color, bar_width=150):
        if maximum <= 0: return
        per = current / maximum
        pygame.draw.rect(self.screen, COLOR_BLACK, (x, y, bar_width, 20))
        if per > 0:
            pygame.draw.rect(self.screen, color, (x, y, int(bar_width * per), 20))
        pygame.draw.rect(self.screen, COLOR_WHITE, (x, y, bar_width, 20), 1)

        text = self.font.render(f"{current}/{maximum}", True, COLOR_WHITE)
        self.screen.blit(text, (x + bar_width // 2 - text.get_width() // 2, y + 2))

    def draw_messages(self, messages):
        y = SCREEN_HEIGHT - 120
        pygame.draw.rect(self.screen, (20, 20, 20), (0, y, SCREEN_WIDTH, 120))
        pygame.draw.line(self.screen, COLOR_WHITE, (0, y), (SCREEN_WIDTH, y))

        msg_height = 20
        start_index = max(0, len(messages) - 5)
        for i, (msg, color) in enumerate(messages[start_index:]):
            text = self.font.render(msg, True, color)
            self.screen.blit(text, (10, y + 10 + i * msg_height))

    def draw_hud(self, player):
        # HP Bar
        self.draw_bar(10, 10, player.fighter.hp, player.fighter.max_hp, COLOR_RED)

        # Stamina Bar
        self.draw_bar(10, 35, player.fighter.stamina, player.fighter.max_stamina, COLOR_GREEN)

        # Level/Depth info could go here

    def draw_menu(self, title, options):
        # Overlay
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, (0, 0))

        # Box
        width = 400
        height = 300
        x = SCREEN_WIDTH // 2 - width // 2
        y = SCREEN_HEIGHT // 2 - height // 2

        pygame.draw.rect(self.screen, COLOR_BLACK, (x, y, width, height))
        pygame.draw.rect(self.screen, COLOR_WHITE, (x, y, width, height), 2)

        title_surf = self.large_font.render(title, True, COLOR_WHITE)
        self.screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, y + 20))

        for i, option in enumerate(options):
            text_surf = self.font.render(f"{i+1}) {option}", True, COLOR_WHITE)
            self.screen.blit(text_surf, (x + 20, y + 80 + i * 30))

    def draw_inventory(self, inventory):
        options = []
        if not inventory.items:
            options.append("Inventory is empty.")
        else:
            for item in inventory.items:
                name = item.name
                if item.equipment and item.equipment.equipped:
                    name += " (E)"
                options.append(name)

        self.draw_menu("Inventory", options)

    def draw_crafting(self, recipes):
        options = []
        if not recipes:
            options.append("No known recipes.")
        else:
            for rec in recipes:
                # Format: Result (Ing1: x, Ing2: y)
                ing_str = ", ".join([f"{k}:{v}" for k,v in rec["ingredients"].items()])
                options.append(f"{rec['result']} [{ing_str}]")

        self.draw_menu("Crafting (Press 1-9 to craft)", options)

    def draw_lore(self, lore_entries):
        # Full screen lore view
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        self.screen.blit(s, (0, 0))

        pygame.draw.rect(self.screen, COLOR_WHITE, (50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), 2)

        title_surf = self.large_font.render("Ancient Lore", True, COLOR_WHITE)
        self.screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 60))

        y = 120
        # Just show random subset or all?
        # For prototype, show first 10 discovered or just random ones from defs for flavor
        for i, entry in enumerate(lore_entries[:12]):
            t = self.font.render(f"{entry['title']}: {entry['text'][:50]}...", True, COLOR_WHITE)
            self.screen.blit(t, (70, y))
            y += 30

        help_surf = self.font.render("Press ESC to return", True, (200, 200, 200))
        self.screen.blit(help_surf, (SCREEN_WIDTH // 2 - help_surf.get_width() // 2, SCREEN_HEIGHT - 40))
