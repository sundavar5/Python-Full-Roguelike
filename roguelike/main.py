import pygame
import sys
import traceback

# Import modules
from roguelike.config import *
from roguelike.game import Game
from roguelike.render import Renderer
from roguelike.ui import UI
from roguelike.combat import handle_player_move, wait_turn, toggle_guard, perform_attack
from roguelike.ai import enemy_turn
from roguelike.items import pickup_item, use_item, drop_item, cast_scroll
from roguelike.crafting import craft_item
from roguelike.dismantle import dismantle_item
from roguelike.data.definitions import RECIPES, LORE
from roguelike.save_load import save_game, load_game

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Generate assets if missing
    import roguelike.assets_gen
    roguelike.assets_gen.main()

    # Initialize subsystems
    renderer = Renderer(screen, "roguelike/assets")
    ui = UI(screen)

    # Try load game or new game
    game = Game()
    game.new_game()

    running = True
    while running:
        # Input handling
        events = pygame.event.get()
        player_turn = False

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                save_game(game)

            if event.type == pygame.KEYDOWN:
                # --- PLAYING STATE ---
                if game.state == STATE_PLAYING:
                    if event.key == KEY_MOVE_UP:
                        player_turn = handle_player_move(0, -1, game)
                    elif event.key == KEY_MOVE_DOWN:
                        player_turn = handle_player_move(0, 1, game)
                    elif event.key == KEY_MOVE_LEFT:
                        player_turn = handle_player_move(-1, 0, game)
                    elif event.key == KEY_MOVE_RIGHT:
                        player_turn = handle_player_move(1, 0, game)
                    elif event.key == KEY_WAIT:
                        player_turn = wait_turn(game)
                    elif event.key == KEY_GUARD:
                        player_turn = toggle_guard(game)
                    elif event.key == KEY_ATTACK_MODE:
                        game.state = STATE_ATTACK_DIRECTION
                        game.add_message("Choose attack direction (WASD).", COLOR_GREEN)
                    elif event.key == KEY_RANGED:
                         game.state = STATE_TARGETING
                         game.target_x, game.target_y = game.player.x, game.player.y
                         game.pending_item = None
                         game.pending_skill = None
                         game.add_message("Targeting Mode (WASD + Enter/T).", COLOR_GREEN)
                    elif event.key == KEY_PICKUP:
                        pickup_item(game)
                        player_turn = True
                    elif event.key == KEY_ENTER:
                        if game.player.x == game.game_map.stairs.x and game.player.y == game.game_map.stairs.y:
                            game.next_level()
                    elif event.key == KEY_INVENTORY:
                        game.state = STATE_INVENTORY
                    elif event.key == KEY_CRAFTING:
                         game.state = STATE_CRAFTING
                    elif event.key == KEY_LORE:
                         game.state = STATE_LORE
                    elif event.key == KEY_CHARACTER:
                         game.state = STATE_CHARACTER_SCREEN
                    elif event.key == KEY_SKILLS:
                         game.state = STATE_SKILLS
                    elif event.key == KEY_ESCAPE:
                        running = False
                        save_game(game)

                # --- ATTACK DIRECTION STATE ---
                elif game.state == STATE_ATTACK_DIRECTION:
                    dx, dy = 0, 0
                    if event.key == KEY_MOVE_UP: dy = -1
                    elif event.key == KEY_MOVE_DOWN: dy = 1
                    elif event.key == KEY_MOVE_LEFT: dx = -1
                    elif event.key == KEY_MOVE_RIGHT: dx = 1
                    elif event.key == KEY_ESCAPE:
                        game.state = STATE_PLAYING
                        game.add_message("Canceled attack.", COLOR_WHITE)

                    if dx != 0 or dy != 0:
                        target = game.get_blocking_entities(game.player.x + dx, game.player.y + dy)
                        if target:
                            perform_attack(game.player, target, game, "heavy")
                            player_turn = True
                        else:
                            game.add_message("You swing at the air.", COLOR_WHITE)
                            player_turn = True
                        game.state = STATE_PLAYING

                # --- TARGETING STATE ---
                elif game.state == STATE_TARGETING:
                    if event.key == KEY_MOVE_UP: game.target_y -= 1
                    elif event.key == KEY_MOVE_DOWN: game.target_y += 1
                    elif event.key == KEY_MOVE_LEFT: game.target_x -= 1
                    elif event.key == KEY_MOVE_RIGHT: game.target_x += 1
                    elif event.key == KEY_ESCAPE:
                        game.state = STATE_PLAYING
                        game.pending_item = None
                        game.pending_skill = None
                    elif event.key == KEY_ENTER or event.key == KEY_TARGET:
                         if game.pending_item:
                             cast_scroll(game.pending_item, game.target_x, game.target_y, game)
                             game.pending_item = None
                             player_turn = True
                             game.state = STATE_PLAYING
                         elif getattr(game, 'pending_skill', None):
                             if game.pending_skill.cast(game.player, game.target_x, game.target_y, game):
                                 player_turn = True
                             game.pending_skill = None
                             game.state = STATE_PLAYING
                         else:
                             # Inspect
                             target = game.get_blocking_entities(game.target_x, game.target_y)
                             if target:
                                 game.add_message(f"You see {target.name}. HP: {target.fighter.hp}/{target.fighter.max_hp}", COLOR_WHITE)
                             else:
                                 tile = game.game_map.tiles[game.target_x][game.target_y]
                                 game.add_message(f"You see {tile.sprite}.", COLOR_WHITE)

                # --- INVENTORY STATE ---
                elif game.state == STATE_INVENTORY:
                    if event.key == KEY_ESCAPE or event.key == KEY_INVENTORY:
                        game.state = STATE_PLAYING
                    elif event.key == KEY_DISMANTLE:
                         game.add_message("Press key (1-9) of item to dismantle.", (255, 200, 0))
                         game.state = 10 # STATE_DISMANTLE_SELECT
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        if idx < len(game.player.inventory.items):
                            item = game.player.inventory.items[idx]
                            use_item(item, game)
                            player_turn = True
                            game.state = STATE_PLAYING

                # --- DISMANTLE SELECT STATE ---
                elif game.state == 10:
                    if event.key == KEY_ESCAPE or event.key == KEY_INVENTORY:
                        game.state = STATE_INVENTORY
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        if idx < len(game.player.inventory.items):
                            item = game.player.inventory.items[idx]
                            if dismantle_item(item, game):
                                player_turn = True
                            game.state = STATE_INVENTORY

                # --- CRAFTING STATE ---
                elif game.state == STATE_CRAFTING:
                    if event.key == KEY_ESCAPE or event.key == KEY_CRAFTING:
                        game.state = STATE_PLAYING
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        if idx < len(RECIPES):
                            success = craft_item(idx, game.player.inventory, game)
                            if success:
                                player_turn = True

                # --- LORE STATE ---
                elif game.state == STATE_LORE:
                    if event.key == KEY_ESCAPE or event.key == KEY_LORE:
                        game.state = STATE_PLAYING

                # --- CHARACTER SCREEN STATE ---
                elif game.state == STATE_CHARACTER_SCREEN:
                    if event.key == KEY_ESCAPE or event.key == KEY_CHARACTER:
                        game.state = STATE_PLAYING
                    elif event.key == KEY_ENTER:
                        if game.player.level.requires_level_up():
                            game.player.level.level_up()
                            game.add_message(f"Welcome to Level {game.player.level.current_level}!", (255, 255, 0))
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_4:
                        if game.player.fighter.attributes.points > 0:
                            idx = event.key - pygame.K_1
                            attr = game.player.fighter.attributes
                            if idx == 0: attr.strength += 1
                            elif idx == 1: attr.dexterity += 1
                            elif idx == 2: attr.constitution += 1
                            elif idx == 3: attr.intelligence += 1
                            attr.points -= 1
                            game.player.fighter.recalculate_stats()

                # --- SKILLS STATE ---
                elif game.state == STATE_SKILLS:
                    if event.key == KEY_ESCAPE or event.key == KEY_SKILLS:
                        game.state = STATE_PLAYING
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        idx = event.key - pygame.K_1
                        if idx < len(game.player.skill_book):
                            skill = game.player.skill_book[idx]

                            if skill.current_cooldown > 0:
                                game.add_message("Skill is on cooldown.", COLOR_RED)
                            elif game.player.fighter.mana < skill.mana_cost:
                                game.add_message("Not enough mana.", COLOR_RED)
                            else:
                                # Pre-check passed
                                game.pending_item = None
                                game.pending_skill = skill
                                game.state = STATE_TARGETING
                                game.target_x, game.target_y = game.player.x, game.player.y
                                game.add_message(f"Targeting {skill.name}...", COLOR_GREEN)

        # Update
        if player_turn and game.state == STATE_PLAYING:
            game.update_effects()
            # Tick skills
            if game.player.skill_book:
                for skill in game.player.skill_book:
                    skill.tick()
            enemy_turn(game)

        if game.fov_recompute:
            renderer.update_fov(game.game_map, game.player)
            game.fov_recompute = False

        # Render
        renderer.render_all(game)
        ui.draw_messages(game.message_log)
        ui.draw_hud(game.player)

        if game.state == STATE_INVENTORY:
            ui.draw_inventory(game.player.inventory)
        elif game.state == 10: # STATE_DISMANTLE
            ui.draw_inventory(game.player.inventory)
            ui.draw_menu("Dismantle Which Item?", [])
        elif game.state == STATE_CRAFTING:
            ui.draw_crafting(RECIPES)
        elif game.state == STATE_LORE:
            ui.draw_lore(LORE)
        elif game.state == STATE_CHARACTER_SCREEN:
            ui.draw_character(game.player)
        elif game.state == STATE_SKILLS:
            ui.draw_skills(game.player.skill_book)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        pygame.quit()
